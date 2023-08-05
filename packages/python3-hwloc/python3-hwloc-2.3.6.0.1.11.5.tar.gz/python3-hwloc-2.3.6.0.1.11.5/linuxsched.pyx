# -*- cython -*-
# -*- coding: utf-8 -*-

#
# Copyright 2011-2017 Red Hat, Inc.
#   This copyrighted material is made available to anyone wishing to use,
#  modify, copy, or redistribute it subject to the terms and conditions of
#  the GNU General Public License v.2.
#
#   This application is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
# Authors:
#   Guy Streeter <guy.streeter@gmail.com>
#
# This exposes the sched_get/setaffinity routines and the bitmap
# structure they use.
#

import os

from posix.unistd cimport pid_t
from libc.stdlib cimport malloc as CMalloc
from libc.string cimport memset as CMemset
from libc.stdlib cimport free as CFree
from libc.errno cimport errno as CErrno
from libc.string cimport strerror as CStrerror

cdef extern from "time.h" nogil:
	ctypedef long time_t
	cdef struct timespec:
		time_t tv_sec
		long tv_nsec

cdef extern from "sched.h":
	int SCHED_OTHER
	int SCHED_FIFO
	int SCHED_RR
	int SCHED_BATCH
	int SCHED_IDLE
	int SCHED_RESET_ON_FORK

	enum: __CPU_SETSIZE
	enum: __NCPUBITS
	ctypedef unsigned long int __cpu_mask
	ctypedef struct cpu_set_t:
		__cpu_mask __bits[__CPU_SETSIZE // __NCPUBITS]
	cdef struct sched_param:
		int sched_priority

	int sched_setparam(pid_t pid, const sched_param *param)
	int sched_getparam(pid_t __pid, sched_param *__param)
	int sched_setscheduler(pid_t __pid, int __policy,
						   const sched_param *__param)
	int sched_getscheduler(pid_t __pid)
	int sched_yield()
	int sched_get_priority_max(int __algorithm)
	int sched_get_priority_min(int __algorithm)
	int sched_rr_get_interval(pid_t __pid, timespec *__t)
	int sched_setaffinity(pid_t __pid, size_t __cpusetsize,
						  const cpu_set_t *__cpuset)
	int sched_getaffinity(pid_t __pid, size_t __cpusetsize,
						  cpu_set_t *__cpuset)

	void CPU_SET(int cpu, cpu_set_t* cpusetp)
	void CPU_CLR(int cpu, cpu_set_t* cpusetp)
	int CPU_ISSET(int cpu, cpu_set_t* cpusetp)

__sched_strings = {
	SCHED_OTHER : "SCHED_OTHER",
	SCHED_FIFO : "SCHED_FIFO",
	SCHED_RR : "SCHED_RR",
	SCHED_BATCH : "SCHED_BATCH",
	SCHED_IDLE : "SCHED_IDLE",
}

__max_cpus = os.sysconf('SC_NPROCESSORS_CONF')

def schedstr(scheduler):
	forkish = ''
	if scheduler & SCHED_RESET_ON_FORK != 0:
		scheduler &= ~SCHED_RESET_ON_FORK
		forkish = '*'
	return __sched_strings.get(scheduler, "UNKNOWN") + forkish

def schedfromstr(string):
	for key in __sched_strings.keys():
		if __sched_strings[key] == string:
			return key
	return 0

cdef void* __checknull(void* p) except NULL:
	if p == NULL:
		raise OSError(CErrno, CStrerror(CErrno))
	return p

def __checkneg1(ret):
	if ret == -1:
		raise OSError(CErrno, CStrerror(CErrno))
	return ret

def GetPriorityMax(int policy):
	return __checkneg1(sched_get_priority_max(policy))

def GetPriorityMin(int policy):
	return __checkneg1(sched_get_priority_min(policy))

def GetPriority(pid_t pid):
	cdef sched_param* p = <sched_param*>__checknull(CMalloc(sizeof(sched_param)))
	CMemset(p, 0, sizeof(sched_param))
	try:
		__checkneg1(sched_getparam(pid, p))
		ret = p.sched_priority
	finally:
		CFree(p)
	return ret

def SetPriority(pid_t pid, int prio):
	cdef sched_param* p = <sched_param*>__checknull(CMalloc(sizeof(sched_param)))
	CMemset(p, 0, sizeof(sched_param))
	p.sched_priority = prio
	try:
		__checkneg1(sched_setparam(pid, p))
	finally:
		CFree(p)

def GetScheduler(pid_t pid):
	return __checkneg1(sched_getscheduler(pid))

def SetScheduler(pid_t pid, int policy, int prio):
	cdef sched_param* p = <sched_param*>__checknull(CMalloc(sizeof(sched_param)))
	CMemset(p, 0, sizeof(sched_param))
	p.sched_priority = prio
	try:
		__checkneg1(sched_setscheduler(pid, policy, p))
	finally:
		CFree(p)

def RRGetInterval(pid_t, pid):
	cdef timespec* t = <timespec*>__checknull(CMalloc(sizeof(timespec)))
	CMemset(t, 0, sizeof(timespec))
	try:
		__checkneg1(sched_rr_get_interval(pid, t))
		sec = t.tv_sec
		nsec = t.tv_nsec
	finally:
		CFree(t)
	return sec, nsec

def Yield():
	return __checkneg1(sched_yield())

cdef __bits_set(cpu_set_t* cpuset):
	s = []
	for i in range(__NCPUBITS):
		if CPU_ISSET(i, cpuset):
			s.append(i)
	return s

def Getaffinity(pid_t pid):
	cdef size_t s = sizeof(cpu_set_t)
	cdef cpu_set_t* c = <cpu_set_t*>__checknull(CMalloc(s))
	CMemset(c, 0, s)
	try:
		__checkneg1(sched_getaffinity(pid, s, c))
		bits = __bits_set(c)
	finally:
		CFree(c)
	return tuple(bits)

def Setaffinity(pid_t pid, mask not None):
	s = sizeof(cpu_set_t)
	cdef cpu_set_t* c = <cpu_set_t*>__checknull(CMalloc(s))
	CMemset(c, 0, s)
	for i in mask:
		CPU_SET(i, c)
	try:
		__checkneg1(sched_setaffinity(pid, s, c))
	finally:
		CFree(c)
