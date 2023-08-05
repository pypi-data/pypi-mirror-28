# -*- cython -*-

#
# Copyright 2013-2017 Red Hat, Inc.
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

DEF WITH_x86_64 = UNAME_MACHINE in [u'x86_64']

__author = 'Guy Streeter <guy.streeter@gmail.com>'
__license = 'GPLv2'
__version = '2.3-1.11.5'
__description = 'Python bindings for hwloc'
__URL = 'https://git.fedorahosted.org/cgit/python-hwloc.git'

from libc.stdio cimport FILE
from posix.unistd cimport pid_t
from libc.stdio cimport fopen as CFopen
from libc.stdio cimport fclose as CFclose
from libc.errno cimport errno as CErrno
from libc.string cimport strerror as bCStrerror
from libc.stdlib cimport malloc as CMalloc
from libc.stdlib cimport free as CFree

from cpython cimport PY_MAJOR_VERSION

def _utfate(text):
	if isinstance(text, unicode):
		return text.encode('utf8')
	if (PY_MAJOR_VERSION < 3) and isinstance(text, str):
		return text.decode('ASCII')
	raise ValueError('requires text input, got %s' % type(text))

def CStrerror(code):
	return str(bCStrerror(code).decode('utf8'))

class HwlocError(Exception):
	pass

class LoadError(HwlocError):
	pass

class NULLError(HwlocError):
	pass

class ArgError(HwlocError):
	"""Exception raised when a calling argument is invalid"""
	def __init__(self, string):
		self.msg = string
	def __str__(self):
		return self.msg

cdef extern from "limits.h":
	enum: INT_MAX
	enum: UINT_MAX

HWLOC_INT_MAX = INT_MAX
HWLOC_UINT_MAX = UINT_MAX

cdef extern from "stdint.h":
	ctypedef int uint64_t

cdef extern from "pthread.h":
	ctypedef unsigned long int pthread_t

# getting around anonymous struct/union stuff
cdef extern from 'hwloc.h':
	cdef struct hwloc_pcidev_attr_s:
		unsigned short domain
		unsigned char bus, dev, func
		unsigned short class_id
		unsigned short vendor_id, device_id, subvendor_id, subdevice_id
		unsigned char revision
		float linkspeed

cdef union ba_upstream:
	hwloc_pcidev_attr_s pci
cdef struct ba_ds_pci:
	unsigned short domain
	unsigned char secondary_bus, subordinate_bus
cdef union ba_downstream:
	ba_ds_pci pci

cdef extern from 'hwloc.h':

####
# hwlocality_bitmap The bitmap API
####
	cdef struct hwloc_bitmap_s:
		pass
	ctypedef hwloc_bitmap_s* hwloc_bitmap_t
	ctypedef const hwloc_bitmap_s* hwloc_const_bitmap_t

	hwloc_bitmap_t hwloc_bitmap_alloc()
	hwloc_bitmap_t hwloc_bitmap_alloc_full()
	void hwloc_bitmap_free(hwloc_bitmap_t bitmap)
	hwloc_bitmap_t hwloc_bitmap_dup(hwloc_const_bitmap_t bitmap)
	void hwloc_bitmap_copy(hwloc_bitmap_t dst, hwloc_const_bitmap_t src)

	int hwloc_bitmap_asprintf(char** strp, hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_sscanf(hwloc_bitmap_t bitmap, const char* string)
	int hwloc_bitmap_list_asprintf(char** strp, hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_list_sscanf(hwloc_bitmap_t bitmap, const char* string)
	int hwloc_bitmap_taskset_asprintf(char** strp, hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_taskset_sscanf(hwloc_bitmap_t bitmap, const char* string)

	void hwloc_bitmap_zero(hwloc_bitmap_t bitmap)
	void hwloc_bitmap_fill(hwloc_bitmap_t bitmap)
	void hwloc_bitmap_only(hwloc_bitmap_t bitmap, unsigned id1)
	void hwloc_bitmap_allbut(hwloc_bitmap_t bitmap, unsigned id1)
	void hwloc_bitmap_from_ith_ulong(hwloc_bitmap_t bitmap, unsigned i,
									 unsigned long mask)

	void hwloc_bitmap_set(hwloc_bitmap_t bitmap, unsigned id1)
	void hwloc_bitmap_set_range(hwloc_bitmap_t bitmap, unsigned begin, int end)
	void hwloc_bitmap_set_ith_ulong(hwloc_bitmap_t bitmap, unsigned i,
									unsigned long mask)
	void hwloc_bitmap_clr(hwloc_bitmap_t bitmap, unsigned id1)
	void hwloc_bitmap_clr_range(hwloc_bitmap_t bitmap, unsigned begin, int end)
	void hwloc_bitmap_singlify(hwloc_bitmap_t bitmap)

	unsigned long hwloc_bitmap_to_ith_ulong(hwloc_const_bitmap_t bitmap, unsigned i)
	int hwloc_bitmap_isset(hwloc_const_bitmap_t bitmap, unsigned id1)
	int hwloc_bitmap_iszero(hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_isfull(hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_first(hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_next(hwloc_const_bitmap_t bitmap, int prev)
	int hwloc_bitmap_last(hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_weight(hwloc_const_bitmap_t bitmap)
	void hwloc_bitmap_or(hwloc_bitmap_t res, hwloc_const_bitmap_t bitmap1,
						 hwloc_const_bitmap_t bitmap2)
	void hwloc_bitmap_and(hwloc_bitmap_t res, hwloc_const_bitmap_t bitmap1,
						  hwloc_const_bitmap_t bitmap2)
	void hwloc_bitmap_andnot(hwloc_bitmap_t res, hwloc_const_bitmap_t bitmap1,
							 hwloc_const_bitmap_t bitmap2)
	void hwloc_bitmap_xor(hwloc_bitmap_t res, hwloc_const_bitmap_t bitmap1,
						  hwloc_const_bitmap_t bitmap2)
	void hwloc_bitmap_not(hwloc_bitmap_t res, hwloc_const_bitmap_t bitmap)
	int hwloc_bitmap_intersects(hwloc_const_bitmap_t bitmap1,
								hwloc_const_bitmap_t bitmap2)
	int hwloc_bitmap_isincluded(hwloc_const_bitmap_t sub_bitmap,
								hwloc_const_bitmap_t super_bitmap)
	int hwloc_bitmap_isequal(hwloc_const_bitmap_t bitmap1,
							 hwloc_const_bitmap_t bitmap2)
	int hwloc_bitmap_compare_first(hwloc_const_bitmap_t bitmap1,
								   hwloc_const_bitmap_t bitmap2)
	int hwloc_bitmap_compare(hwloc_const_bitmap_t bitmap1,
							 hwloc_const_bitmap_t bitmap2)

####
# API version
####
	enum: HWLOC_API_VERSION
	unsigned hwloc_get_api_version()

####
# Topology context
####
	cdef struct hwloc_topology:
		pass
	ctypedef hwloc_topology* hwloc_topology_t

####
# Object sets
####
	ctypedef hwloc_bitmap_t hwloc_cpuset_t
	ctypedef hwloc_const_bitmap_t hwloc_const_cpuset_t
	ctypedef hwloc_bitmap_t hwloc_nodeset_t
	ctypedef hwloc_const_bitmap_t hwloc_const_nodeset_t

####
# Topology Object types
####
	ctypedef enum hwloc_obj_type_t:
		HWLOC_OBJ_SYSTEM
		HWLOC_OBJ_MACHINE
		HWLOC_OBJ_NUMANODE
		HWLOC_OBJ_PACKAGE
		HWLOC_OBJ_CACHE
		HWLOC_OBJ_CORE
		HWLOC_OBJ_PU
		HWLOC_OBJ_GROUP
		HWLOC_OBJ_MISC
		HWLOC_OBJ_BRIDGE
		HWLOC_OBJ_PCI_DEVICE
		HWLOC_OBJ_OS_DEVICE
		HWLOC_OBJ_TYPE_MAX
	ctypedef enum hwloc_obj_cache_type_t:
		HWLOC_OBJ_CACHE_UNIFIED
		HWLOC_OBJ_CACHE_DATA
		HWLOC_OBJ_CACHE_INSTRUCTION
	ctypedef enum hwloc_obj_bridge_type_t:
		HWLOC_OBJ_BRIDGE_HOST
		HWLOC_OBJ_BRIDGE_PCI
	ctypedef enum hwloc_obj_osdev_type_t:
		HWLOC_OBJ_OSDEV_BLOCK
		HWLOC_OBJ_OSDEV_GPU
		HWLOC_OBJ_OSDEV_NETWORK
		HWLOC_OBJ_OSDEV_OPENFABRICS
		HWLOC_OBJ_OSDEV_DMA
		HWLOC_OBJ_OSDEV_COPROC

	int hwloc_compare_types (hwloc_obj_type_t type1, hwloc_obj_type_t type2)
	cdef enum hwloc_compare_types_e:
		HWLOC_TYPE_UNORDERED = INT_MAX

####
# Topology Objects
####
	cdef struct hwloc_obj_memory_page_type_s:
		uint64_t size
		uint64_t count
	cdef struct hwloc_obj_memory_s:
		uint64_t total_memory
		uint64_t local_memory
		unsigned page_types_len
		hwloc_obj_memory_page_type_s* page_types
	cdef struct hwloc_cache_attr_s:
		uint64_t size
		unsigned depth
		unsigned linesize
		int associativity
		hwloc_obj_cache_type_t type
	cdef struct hwloc_group_attr_s:
		unsigned depth
	cdef struct hwloc_bridge_attr_s:
		ba_upstream upstream
		hwloc_obj_bridge_type_t upstream_type
		ba_downstream downstream
		hwloc_obj_bridge_type_t downstream_type
		int depth
	cdef struct hwloc_osdev_attr_s:
		hwloc_obj_osdev_type_t type
	cdef union hwloc_obj_attr_u:
		hwloc_cache_attr_s cache
		hwloc_group_attr_s group
		hwloc_pcidev_attr_s pcidev
		hwloc_bridge_attr_s bridge
		hwloc_osdev_attr_s osdev
	cdef struct hwloc_distances_s:
		unsigned relative_depth
		unsigned nbobjs
		float* latency
		float latency_max
		float latency_base
	cdef struct hwloc_obj_info_s:
		char* name
		char* value
	cdef struct hwloc_obj:
		hwloc_obj_type_t type
		unsigned os_index
		char* name
		hwloc_obj_memory_s memory
		hwloc_obj_attr_u *attr
		unsigned depth
		unsigned logical_index
		int os_level
		hwloc_obj* next_cousin
		hwloc_obj* prev_cousin
		hwloc_obj* parent
		unsigned sibling_rank
		hwloc_obj* next_sibling
		hwloc_obj* prev_sibling
		unsigned arity
		hwloc_obj** children
		hwloc_obj* first_child
		hwloc_obj* last_child
		void* userdata
		hwloc_cpuset_t cpuset
		hwloc_cpuset_t complete_cpuset
		hwloc_cpuset_t online_cpuset
		hwloc_cpuset_t allowed_cpuset
		hwloc_nodeset_t nodeset
		hwloc_nodeset_t complete_nodeset
		hwloc_nodeset_t allowed_nodeset
		hwloc_distances_s** distances
		unsigned distances_count
		hwloc_obj_info_s* infos
		unsigned infos_count
		int symmetric_subtree
	ctypedef hwloc_obj* hwloc_obj_t

	ctypedef pid_t hwloc_pid_t
	ctypedef pthread_t hwloc_thread_t

####
# Topology Creation and Destruction
####
	int hwloc_topology_init(hwloc_topology_t* topologypp)
	int hwloc_topology_load(hwloc_topology_t topology)
	void hwloc_topology_destroy(hwloc_topology_t topology)
	void hwloc_topology_check(hwloc_topology_t topology)

####
# Topology Detection Configuration and Query
####
	int hwloc_topology_ignore_type(hwloc_topology_t topology,
								   hwloc_obj_type_t type1)
	int hwloc_topology_ignore_type_keep_structure(hwloc_topology_t topology,
												  hwloc_obj_type_t type1)
	int hwloc_topology_ignore_all_keep_structure(hwloc_topology_t topology)
	cdef enum hwloc_topology_flags_e:
		HWLOC_TOPOLOGY_FLAG_WHOLE_SYSTEM = (1UL<<0)
		HWLOC_TOPOLOGY_FLAG_IS_THISSYSTEM = (1UL<<1)
		HWLOC_TOPOLOGY_FLAG_IO_DEVICES = (1UL<<2)
		HWLOC_TOPOLOGY_FLAG_IO_BRIDGES = (1UL<<3)
		HWLOC_TOPOLOGY_FLAG_WHOLE_IO = (1UL<<4)
		HWLOC_TOPOLOGY_FLAG_ICACHES = (1UL<<5)
	int hwloc_topology_set_flags(hwloc_topology_t topology, unsigned long flags)
	int hwloc_topology_set_pid(hwloc_topology_t topology, hwloc_pid_t pid)
	int hwloc_topology_set_fsroot(hwloc_topology_t topology,
								  const char* fsroot_path)
	int hwloc_topology_set_synthetic(hwloc_topology_t topology,
									 const char* description)
	int hwloc_topology_set_xml(hwloc_topology_t topology, const char* xmlpath)
	int hwloc_topology_set_xmlbuffer(hwloc_topology_t topology, const char* buffer1,
									 int size)
	int hwloc_topology_set_custom(hwloc_topology_t topology)
	int hwloc_topology_set_distance_matrix(hwloc_topology_t topology,
										   hwloc_obj_type_t type1, unsigned nbobjs,
										   unsigned* os_index, float* distances)
	int hwloc_topology_is_thissystem(hwloc_topology_t topology)
	cdef struct hwloc_topology_discovery_support:
		unsigned char pu
	cdef struct hwloc_topology_cpubind_support:
		unsigned char set_thisproc_cpubind
		unsigned char get_thisproc_cpubind
		unsigned char set_proc_cpubind
		unsigned char get_proc_cpubind
		unsigned char set_thisthread_cpubind
		unsigned char get_thisthread_cpubind
		unsigned char set_thread_cpubind
		unsigned char get_thread_cpubind
		unsigned char get_thisproc_last_cpu_location
		unsigned char get_proc_last_cpu_location
		unsigned char get_thisthread_last_cpu_location
	cdef struct hwloc_topology_membind_support:
		unsigned char set_thisproc_membind
		unsigned char get_thisproc_membind
		unsigned char set_proc_membind
		unsigned char get_proc_membind
		unsigned char set_thisthread_membind
		unsigned char get_thisthread_membind
		unsigned char set_area_membind
		unsigned char get_area_membind
		unsigned char alloc_membind
		unsigned char firsttouch_membind
		unsigned char bind_membind
		unsigned char interleave_membind
		unsigned char replicate_membind
		unsigned char nexttouch_membind
		unsigned char migrate_membind
		unsigned char get_area_memlocation
	cdef struct hwloc_topology_support:
		hwloc_topology_discovery_support* discovery
		hwloc_topology_cpubind_support* cpubind
		hwloc_topology_membind_support* membind
	const hwloc_topology_support* hwloc_topology_get_support(hwloc_topology_t topology)
	void hwloc_topology_set_userdata(hwloc_topology_t topology, const void *userdata)
	void * hwloc_topology_get_userdata(hwloc_topology_t topology)

####
# Object levels, depths and types
####
	unsigned int hwloc_topology_get_depth(hwloc_topology_t topology)
	int hwloc_get_type_depth(hwloc_topology_t topology, hwloc_obj_type_t type1)
	int hwloc_get_type_or_below_depth(hwloc_topology_t topology,
									  hwloc_obj_type_t type1)
	int hwloc_get_type_or_above_depth(hwloc_topology_t topology,
									  hwloc_obj_type_t type1)

	cdef enum hwloc_get_type_depth_e:
		HWLOC_TYPE_DEPTH_UNKNOWN = -1
		HWLOC_TYPE_DEPTH_MULTIPLE = -2
		HWLOC_TYPE_DEPTH_BRIDGE = -3
		HWLOC_TYPE_DEPTH_PCI_DEVICE = -4
		HWLOC_TYPE_DEPTH_OS_DEVICE = -5
	hwloc_obj_type_t hwloc_get_depth_type(hwloc_topology_t topology, unsigned depth)
	unsigned hwloc_get_nbobjs_by_depth(hwloc_topology_t topology, int depth)
	int hwloc_get_nbobjs_by_type(hwloc_topology_t topology, hwloc_obj_type_t type1)
	hwloc_obj_t hwloc_get_root_obj(hwloc_topology_t topology)
	hwloc_obj_t hwloc_get_obj_by_depth(hwloc_topology_t topology, int depth,
									   unsigned idx)
	hwloc_obj_t hwloc_get_obj_by_type(hwloc_topology_t topology,
									  hwloc_obj_type_t type1, unsigned idx)
	hwloc_obj_t hwloc_get_next_obj_by_depth(hwloc_topology_t topology,
											int depth, hwloc_obj_t prev)
	hwloc_obj_t hwloc_get_next_obj_by_type(hwloc_topology_t topology,
										   hwloc_obj_type_t type1, hwloc_obj_t prev)
	unsigned long hwloc_topology_get_flags(hwloc_topology_t topology)

####
# Manipulating Object Type, Sets and Attributes as Strings
####
	const char* hwloc_obj_type_string (hwloc_obj_type_t type1)
	int hwloc_obj_type_sscanf(const char *string, hwloc_obj_type_t *typep,
							  int *depthattrp, void *typeattrp, size_t typeattrsize)
	int hwloc_obj_type_snprintf(char* string, size_t size, hwloc_obj_t obj,
								int verbose)
	int hwloc_obj_attr_snprintf(char* string, size_t size, hwloc_obj_t obj,
								const char* separator, int verbose)
	int hwloc_obj_cpuset_snprintf(char* string, size_t size, size_t nobj,
								  const hwloc_obj_t* objs)
	const char* hwloc_obj_get_info_by_name(hwloc_obj_t obj, const char* name)
	void hwloc_obj_add_info(hwloc_obj_t obj, const char *name, const char* value)
	# deprecated:
	hwloc_obj_type_t hwloc_obj_type_of_string(const char* string)
	int hwloc_obj_snprintf(char* string, size_t size, hwloc_topology_t topology,
						   hwloc_obj_t obj, const char* indexprefix, int verbose)

####
# CPU binding
####
	ctypedef enum hwloc_cpubind_flags_t:
		HWLOC_CPUBIND_PROCESS = (1<<0)
		HWLOC_CPUBIND_THREAD = (1<<1)
		HWLOC_CPUBIND_STRICT = (1<<2)
		HWLOC_CPUBIND_NOMEMBIND = (1<<3)
	int hwloc_set_cpubind(hwloc_topology_t topology, hwloc_const_cpuset_t set1, int flags)
	int hwloc_get_cpubind(hwloc_topology_t topology, hwloc_cpuset_t set1, int flags)
	int hwloc_set_proc_cpubind(hwloc_topology_t topology, hwloc_pid_t pid,
							   hwloc_const_cpuset_t set1, int flags)
	int hwloc_get_proc_cpubind(hwloc_topology_t topology, hwloc_pid_t pid,
							   hwloc_cpuset_t set1, int flags)
	int hwloc_set_thread_cpubind(hwloc_topology_t topology, hwloc_thread_t thread,
								 hwloc_const_cpuset_t set1, int flags)
	int hwloc_get_thread_cpubind(hwloc_topology_t topology, hwloc_thread_t thread,
								 hwloc_cpuset_t set1, int flags)
	int hwloc_get_last_cpu_location(hwloc_topology_t topology, hwloc_cpuset_t set1,
									int flags)
	int hwloc_get_proc_last_cpu_location(hwloc_topology_t topology,
										 hwloc_pid_t pid, hwloc_cpuset_t set1,
										 int flags)

####
# Memory binding policy
####
	ctypedef enum hwloc_membind_policy_t:
		HWLOC_MEMBIND_DEFAULT
		HWLOC_MEMBIND_FIRSTTOUCH
		HWLOC_MEMBIND_BIND
		HWLOC_MEMBIND_INTERLEAVE
		HWLOC_MEMBIND_REPLICATE
		HWLOC_MEMBIND_NEXTTOUCH
		HWLOC_MEMBIND_MIXED = -1
	int hwloc_set_membind_nodeset(hwloc_topology_t topology,
								  hwloc_const_nodeset_t nodeset,
								  hwloc_membind_policy_t policy, int flags)
	int hwloc_set_membind(hwloc_topology_t topology, hwloc_const_cpuset_t cpuset,
						  hwloc_membind_policy_t policy, int flags)
	int hwloc_get_membind_nodeset(hwloc_topology_t topology,
								  hwloc_bitmap_t set,
								  hwloc_membind_policy_t* policy, int flags)
	int hwloc_get_membind(hwloc_topology_t topology, hwloc_bitmap_t set,
						  hwloc_membind_policy_t* policy, int flags)
	int hwloc_set_proc_membind_nodeset(hwloc_topology_t topology, hwloc_pid_t pid,
									   hwloc_const_nodeset_t nodeset,
									   hwloc_membind_policy_t policy, int flags)
	int hwloc_set_proc_membind(hwloc_topology_t topology, hwloc_pid_t pid,
							   hwloc_const_bitmap_t set,
							   hwloc_membind_policy_t policy, int flags)
	int hwloc_get_proc_membind_nodeset(hwloc_topology_t topology,
									   hwloc_pid_t pid, hwloc_nodeset_t nodeset,
									   hwloc_membind_policy_t* policy, int flags)
	int hwloc_get_proc_membind(hwloc_topology_t topology, hwloc_pid_t pid,
							   hwloc_bitmap_t set,
							   hwloc_membind_policy_t* policy, int flags)
	int hwloc_set_area_membind_nodeset(hwloc_topology_t topology, const void* addr,
									   size_t len1, hwloc_const_nodeset_t nodeset,
									   hwloc_membind_policy_t policy, int flags)
	int hwloc_set_area_membind(hwloc_topology_t topology, const void* addr,
							   size_t len1, hwloc_const_bitmap_t set,
							   hwloc_membind_policy_t policy, int flags)
	int hwloc_get_area_membind_nodeset(hwloc_topology_t topology, const void* addr,
									   size_t len, hwloc_nodeset_t nodeset,
									   hwloc_membind_policy_t* policy, int flags)
	int hwloc_get_area_membind(hwloc_topology_t topology, const void* addr,
							   size_t len, hwloc_bitmap_t set,
							   hwloc_membind_policy_t* policy, int flags)
	int hwloc_get_area_memlocation(hwloc_topology_t topology, const void *addr,
								   size_t len, hwloc_bitmap_t set, int flags)
	void* hwloc_alloc(hwloc_topology_t topology, size_t len1)
	void* hwloc_alloc_membind_nodeset(hwloc_topology_t topology, size_t len1,
									  hwloc_const_nodeset_t nodeset,
									  hwloc_membind_policy_t policy, int flags)
	void* hwloc_alloc_membind(hwloc_topology_t topology, size_t len1,
							  hwloc_const_bitmap_t set,
							  hwloc_membind_policy_t policy, int flags)
	void* hwloc_alloc_membind_policy_nodeset(hwloc_topology_t topology,
											 size_t len1,
											 hwloc_const_nodeset_t nodeset,
											 hwloc_membind_policy_t policy,
											 int flags)
	void* hwloc_alloc_membind_policy(hwloc_topology_t topology, size_t len1,
									 hwloc_const_bitmap_t set,
									 hwloc_membind_policy_t policy, int flags)
	int hwloc_free(hwloc_topology_t topology, void* addr, size_t len1)

####
# Modifying a loaded Topology
####
	hwloc_obj_t hwloc_topology_insert_misc_object_by_cpuset(hwloc_topology_t topology,
															hwloc_const_cpuset_t cpuset,
															const char *name)
	hwloc_obj_t hwloc_topology_insert_misc_object_by_parent(hwloc_topology_t topology,
															hwloc_obj_t parent,
															const char *name)
	cdef enum hwloc_restrict_flags_e:
		HWLOC_RESTRICT_FLAG_ADAPT_DISTANCES = (1<<0)
		HWLOC_RESTRICT_FLAG_ADAPT_MISC = (1<<1)
		HWLOC_RESTRICT_FLAG_ADAPT_IO = (1<<2)
	int hwloc_topology_restrict(hwloc_topology_t topology,
								hwloc_const_cpuset_t cpuset, unsigned long flags)
	int hwloc_topology_dup(hwloc_topology_t *newtopology,
						   hwloc_topology_t oldtopology)

####
# Building Custom Topologies
####
	int hwloc_custom_insert_topology(hwloc_topology_t newtopology,
									 hwloc_obj_t newparent,
									 hwloc_topology_t oldtopology,
									 hwloc_obj_t oldroot)
	hwloc_obj_t hwloc_custom_insert_group_object_by_parent(hwloc_topology_t topology,
														   hwloc_obj_t parent,
														   int groupdepth)

####
# Exporting Topologies to XML
####
	int hwloc_topology_export_xml(hwloc_topology_t topology, const char* xmlpath)
	int hwloc_topology_export_xmlbuffer(hwloc_topology_t topology, char** xmlbuffer,
										int *buflen)
	void hwloc_free_xmlbuffer(hwloc_topology_t topology, char* xmlbuffer)
	void hwloc_topology_set_userdata_export_callback(hwloc_topology_t topology,
													 void (*export_cb)(void* reserved,
																	   hwloc_topology_t topology,
																	   hwloc_obj_t obj))
	int hwloc_export_obj_userdata(void* reserved, hwloc_topology_t topology,
								  hwloc_obj_t obj, const char* name,
								  const void* buffer1, size_t length)
	int hwloc_export_obj_userdata_base64(void *reserved, hwloc_topology_t topology,
										 hwloc_obj_t obj, const char *name,
										 const void *buffer1, size_t length)
	void hwloc_topology_set_userdata_import_callback(hwloc_topology_t topology,
													 void (*import_cb)(hwloc_topology_t topology,
																	   hwloc_obj_t obj,
																	   const char* name,
																	   const void* buffer1,
																	   size_t length))

####
# Exporting Topologies to Synthetic
####
	cdef enum hwloc_topology_export_synthetic_flags_e:
		HWLOC_TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_EXTENDED_TYPES = (1<<0)
		HWLOC_TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_ATTRS = (1<<1)
	int hwloc_topology_export_synthetic(hwloc_topology_t topology, char *buffer,
										size_t buflen, unsigned long flags)

####
# Finding Objects Inside a CPU set
####
	hwloc_obj_t hwloc_get_first_largest_obj_inside_cpuset(hwloc_topology_t topology,
													  hwloc_const_cpuset_t set1)
	int hwloc_get_largest_objs_inside_cpuset(hwloc_topology_t topology,
											 hwloc_const_cpuset_t set1,
											 hwloc_obj_t* objs, int max1)
	hwloc_obj_t hwloc_get_next_obj_inside_cpuset_by_depth(hwloc_topology_t topology,
														  hwloc_const_cpuset_t set1,
														  int depth,
														  hwloc_obj_t prev)
	hwloc_obj_t hwloc_get_next_obj_inside_cpuset_by_type(hwloc_topology_t topology,
														 hwloc_const_cpuset_t set1,
														 hwloc_obj_type_t type1,
														 hwloc_obj_t prev)
	hwloc_obj_t hwloc_get_obj_inside_cpuset_by_depth(hwloc_topology_t topology,
													 hwloc_const_cpuset_t set1,
													 int depth, unsigned idx)
	hwloc_obj_t hwloc_get_obj_inside_cpuset_by_type(hwloc_topology_t topology,
													hwloc_const_cpuset_t set1,
													hwloc_obj_type_t type1,
													unsigned idx)
	unsigned hwloc_get_nbobjs_inside_cpuset_by_depth(hwloc_topology_t topology,
													 hwloc_const_cpuset_t set1,
													 int depth)
	int hwloc_get_nbobjs_inside_cpuset_by_type(hwloc_topology_t topology,
											   hwloc_const_cpuset_t set1,
											   hwloc_obj_type_t type1)
	int hwloc_get_obj_index_inside_cpuset(hwloc_topology_t topology,
										  hwloc_const_cpuset_t set1,
										  hwloc_obj_t obj)

####
# Finding a single Object covering at least a CPU set
####
	hwloc_obj_t hwloc_get_child_covering_cpuset(hwloc_topology_t topology,
											hwloc_const_cpuset_t set1,
											hwloc_obj_t parent)
	hwloc_obj_t hwloc_get_obj_covering_cpuset(hwloc_topology_t topology,
											  hwloc_const_cpuset_t set1)
	hwloc_obj_t hwloc_get_next_obj_covering_cpuset_by_depth(hwloc_topology_t topology,
															hwloc_const_cpuset_t set1,
															int depth,
															hwloc_obj_t prev)
	hwloc_obj_t hwloc_get_next_obj_covering_cpuset_by_type(hwloc_topology_t topology,
														   hwloc_const_cpuset_t set1,
														   hwloc_obj_type_t type1,
														   hwloc_obj_t prev)

####
# Looking at Ancestor and Child Objects
####
	hwloc_obj_t hwloc_get_ancestor_obj_by_depth(hwloc_topology_t topology,
												int depth, hwloc_obj_t obj)
	hwloc_obj_t hwloc_get_ancestor_obj_by_type(hwloc_topology_t topology,
											   hwloc_obj_type_t type1,
											   hwloc_obj_t obj)
	hwloc_obj_t hwloc_get_common_ancestor_obj(hwloc_topology_t topology,
											  hwloc_obj_t obj1, hwloc_obj_t obj2)
	int hwloc_obj_is_in_subtree(hwloc_topology_t topology, hwloc_obj_t obj,
								hwloc_obj_t subtree_root)
	hwloc_obj_t hwloc_get_next_child(hwloc_topology_t topology, hwloc_obj_t parent,
									 hwloc_obj_t prev)

####
# Looking at Cache Objects
####
	int hwloc_get_cache_type_depth(hwloc_topology_t topology,
								   unsigned cachelevel,
								   hwloc_obj_cache_type_t cachetype)
	hwloc_obj_t hwloc_get_cache_covering_cpuset(hwloc_topology_t topology,
												hwloc_const_cpuset_t set1)
	hwloc_obj_t hwloc_get_shared_cache_covering_obj(hwloc_topology_t topology,
													hwloc_obj_t obj)

####
# Finding objects, miscellaneous helpers
####
	hwloc_obj_t hwloc_get_pu_obj_by_os_index(hwloc_topology_t topology,
											 unsigned os_index)
	hwloc_obj_t hwloc_get_numanode_obj_by_os_index(hwloc_topology_t topology,
												   unsigned os_index)
	unsigned hwloc_get_closest_objs(hwloc_topology_t topology, hwloc_obj_t src,
									hwloc_obj_t* objs, unsigned max1)
	hwloc_obj_t hwloc_get_obj_below_by_type(hwloc_topology_t topology,
											hwloc_obj_type_t type1, unsigned idx1,
											hwloc_obj_type_t type2, unsigned idx2)
	hwloc_obj_t hwloc_get_obj_below_array_by_type(hwloc_topology_t topology, int nr,
												  hwloc_obj_type_t *typev,
												  unsigned *idxv)

####
# Distributing items over a topology
####
	ctypedef enum hwloc_distrib_flags_e:
		HWLOC_DISTRIB_FLAG_REVERSE = (1<<0)
	int hwloc_distrib(hwloc_topology_t topology, hwloc_obj_t *roots,
					  unsigned n_roots, hwloc_cpuset_t *set, unsigned n,
					  unsigned until, unsigned long flags)

####
# Binding Helpers (deprecated)
####
	void hwloc_distribute(hwloc_topology_t topology, hwloc_obj_t root,
						  hwloc_cpuset_t *set1, unsigned n, unsigned until)
	void hwloc_distributev(hwloc_topology_t topology, hwloc_obj_t *roots,
						   unsigned n_roots, hwloc_cpuset_t *set, unsigned n,
						   unsigned until)


####
# CPU and node sets of entire topologies
####
	hwloc_const_cpuset_t hwloc_topology_get_complete_cpuset(hwloc_topology_t topology)
	hwloc_const_cpuset_t hwloc_topology_get_topology_cpuset(hwloc_topology_t topology)
	hwloc_const_cpuset_t hwloc_topology_get_online_cpuset(hwloc_topology_t topology)
	hwloc_const_cpuset_t hwloc_topology_get_allowed_cpuset(hwloc_topology_t topology)
	hwloc_const_nodeset_t hwloc_topology_get_complete_nodeset(hwloc_topology_t topology)
	hwloc_const_nodeset_t hwloc_topology_get_topology_nodeset(hwloc_topology_t topology)
	hwloc_const_nodeset_t hwloc_topology_get_allowed_nodeset(hwloc_topology_t topology)

####
# Converting between CPU sets and node sets
####
	void hwloc_cpuset_to_nodeset(hwloc_topology_t topology,
								 hwloc_const_cpuset_t _cpuset,
								 hwloc_nodeset_t nodeset)
	void hwloc_cpuset_to_nodeset_strict(hwloc_topology_t topology,
										hwloc_const_cpuset_t _cpuset,
										hwloc_nodeset_t nodeset)
	void hwloc_cpuset_from_nodeset(hwloc_topology_t topology,
								   hwloc_cpuset_t _cpuset,
								   hwloc_const_nodeset_t nodeset)
	void hwloc_cpuset_from_nodeset_strict(hwloc_topology_t topology,
										  hwloc_cpuset_t _cpuset,
										  hwloc_const_nodeset_t nodeset)

####
# Manipulating Distances
####
	const hwloc_distances_s* hwloc_get_whole_distance_matrix_by_depth(hwloc_topology_t topology,
																	  int depth)
	const hwloc_distances_s* hwloc_get_whole_distance_matrix_by_type(hwloc_topology_t topology,
																	 hwloc_obj_type_t type1)
	const hwloc_distances_s* hwloc_get_distance_matrix_covering_obj_by_depth(hwloc_topology_t topology,
																			 hwloc_obj_t obj,
																			 int depth,
																			 unsigned *firstp)
	int hwloc_get_latency(hwloc_topology_t topology, hwloc_obj_t obj1,
						  hwloc_obj_t obj2, float *latency, float *reverse_latency)

####
# Finding I/O objects
####
	hwloc_obj_t hwloc_get_non_io_ancestor_obj(hwloc_topology_t topology,
											  hwloc_obj_t ioobj)
	hwloc_obj_t hwloc_get_next_pcidev(hwloc_topology_t topology, hwloc_obj_t prev)
	hwloc_obj_t hwloc_get_pcidev_by_busid(hwloc_topology_t topology,
										  unsigned domain, unsigned bus,
										  unsigned dev, unsigned func)
	hwloc_obj_t hwloc_get_pcidev_by_busidstring(hwloc_topology_t topology,
												const char *busid)
	hwloc_obj_t hwloc_get_next_osdev(hwloc_topology_t topology, hwloc_obj_t prev)
	hwloc_obj_t hwloc_get_next_bridge(hwloc_topology_t topology, hwloc_obj_t prev)
	int hwloc_bridge_covers_pcibus(hwloc_obj_t bridge, unsigned domain,
								   unsigned bus)
	hwloc_obj_t hwloc_get_hostbridge_by_pcibus(hwloc_topology_t topology,
											   unsigned domain, unsigned bus)

####
# Topology differences
####
	cdef enum hwloc_topology_diff_obj_attr_type_e:
		HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_SIZE
		HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_NAME
		HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_INFO
	ctypedef hwloc_topology_diff_obj_attr_type_e hwloc_topology_diff_obj_attr_type_t
	cdef struct hwloc_topology_diff_obj_attr_generic_s:
		hwloc_topology_diff_obj_attr_type_t type
	cdef struct hwloc_topology_diff_obj_attr_uint64_s:
		hwloc_topology_diff_obj_attr_type_t type
		uint64_t index
		uint64_t oldvalue
		uint64_t newvalue
	cdef struct hwloc_topology_diff_obj_attr_string_s:
		hwloc_topology_diff_obj_attr_type_t type
		char *name
		char *oldvalue
		char *newvalue
	cdef union hwloc_topology_diff_obj_attr_u:
		hwloc_topology_diff_obj_attr_generic_s generic
		hwloc_topology_diff_obj_attr_uint64_s attr_utin64
		hwloc_topology_diff_obj_attr_string_s string
	cdef enum hwloc_topology_diff_type_e:
		HWLOC_TOPOLOGY_DIFF_OBJ_ATTR
		HWLOC_TOPOLOGY_DIFF_TOO_COMPLEX
	ctypedef hwloc_topology_diff_type_e hwloc_topology_diff_type_t
	cdef union hwloc_topology_diff_u
	cdef struct hwloc_topology_diff_generic_s:
		hwloc_topology_diff_type_t type
		hwloc_topology_diff_u *next
	cdef struct hwloc_topology_diff_obj_attr_s:
		hwloc_topology_diff_type_t type
		hwloc_topology_diff_u *next
		unsigned obj_depth
		unsigned obj_index
		hwloc_topology_diff_obj_attr_u diff
	cdef struct hwloc_topology_diff_too_complex_s:
		hwloc_topology_diff_type_t type
		hwloc_topology_diff_u *next
		unsigned obj_depth
		unsigned obj_index
	cdef union hwloc_topology_diff_u:
		hwloc_topology_diff_generic_s generic
		hwloc_topology_diff_obj_attr_s obj_attr
		hwloc_topology_diff_too_complex_s too_complex
	ctypedef hwloc_topology_diff_u *hwloc_topology_diff_t
	int hwloc_topology_diff_build(hwloc_topology_t topology,
								  hwloc_topology_t newtopology,
								  unsigned long flags, hwloc_topology_diff_t *diff)
	cdef enum hwloc_topology_diff_apply_flags_e:
		HWLOC_TOPOLOGY_DIFF_APPLY_REVERSE = (1<<0)
	int hwloc_topology_diff_apply(hwloc_topology_t topology,
								  hwloc_topology_diff_t diff, unsigned long flags)
	int hwloc_topology_diff_destroy(hwloc_topology_t topology,
									hwloc_topology_diff_t diff)
	int hwloc_topology_diff_load_xml(hwloc_topology_t topology, const char *xmlpath,
									 hwloc_topology_diff_t *diff, char **refname)
	int hwloc_topology_diff_export_xml(hwloc_topology_t topology,
									   hwloc_topology_diff_t diff,
									   const char *refname, const char *xmlpath)
	int hwloc_topology_diff_load_xmlbuffer(hwloc_topology_t topology,
										   const char *xmlbuffer, int buflen,
										   hwloc_topology_diff_t *diff,
										   char **refname)
	int hwloc_topology_diff_export_xmlbuffer(hwloc_topology_t topology,
											 hwloc_topology_diff_t diff,
											 const char *refname,
											 char **xmlbuffer, int *buflen)

####
# Linux-only helpers
####
	int hwloc_linux_parse_cpumap_file(FILE* file, hwloc_cpuset_t set1)
	int hwloc_linux_set_tid_cpubind(hwloc_topology_t topology, pid_t tid,
									hwloc_const_cpuset_t set1)
	int hwloc_linux_get_tid_cpubind(hwloc_topology_t topology, pid_t tid,
									hwloc_cpuset_t set1)
	int hwloc_linux_get_tid_last_cpu_location(hwloc_topology_t topology,
											  pid_t tid, hwloc_bitmap_t set_)


cdef extern from 'hwloc/gl.h':
####
# Interoperability with OpenGL displays
####
	hwloc_obj_t hwloc_gl_get_display_osdev_by_port_device(hwloc_topology_t topology,
														  unsigned port,
														  unsigned device)
	hwloc_obj_t hwloc_gl_get_display_osdev_by_name(hwloc_topology_t topology,
												   const char* name)
	int hwloc_gl_get_display_by_osdev(hwloc_topology_t topology, hwloc_obj_t osdev,
									  unsigned *port, unsigned *device)


#	cdef enum hwloc_membind_flags_t:
HWLOC_MEMBIND_PROCESS = (1<<0)
HWLOC_MEMBIND_THREAD = (1<<1)
HWLOC_MEMBIND_STRICT = (1<<2)
HWLOC_MEMBIND_MIGRATE = (1<<3)
HWLOC_MEMBIND_NOCPUBIND = (1<<4)
HWLOC_MEMBIND_BYNODESET = (1<<5)


HWLOC_OBJ_NODE = HWLOC_OBJ_NUMANODE
HWLOC_OBJ_SOCKET = HWLOC_OBJ_PACKAGE

OBJ_SYSTEM = HWLOC_OBJ_SYSTEM
OBJ_MACHINE = HWLOC_OBJ_MACHINE
OBJ_NUMANODE = HWLOC_OBJ_NUMANODE
OBJ_PACKAGE = HWLOC_OBJ_PACKAGE
OBJ_NODE = HWLOC_OBJ_NODE
OBJ_SOCKET = HWLOC_OBJ_SOCKET
OBJ_CACHE = HWLOC_OBJ_CACHE
OBJ_CORE = HWLOC_OBJ_CORE
OBJ_PU = HWLOC_OBJ_PU
OBJ_GROUP = HWLOC_OBJ_GROUP
OBJ_MISC = HWLOC_OBJ_MISC
OBJ_BRIDGE = HWLOC_OBJ_BRIDGE
OBJ_PCI_DEVICE = HWLOC_OBJ_PCI_DEVICE
OBJ_OS_DEVICE = HWLOC_OBJ_OS_DEVICE
OBJ_TYPE_MAX = HWLOC_OBJ_TYPE_MAX

OBJ_CACHE_UNIFIED = HWLOC_OBJ_CACHE_UNIFIED
OBJ_CACHE_DATA = HWLOC_OBJ_CACHE_DATA
OBJ_CACHE_INSTRUCTION = HWLOC_OBJ_CACHE_INSTRUCTION

OBJ_BRIDGE_HOST = HWLOC_OBJ_BRIDGE_HOST
OBJ_BRIDGE_PCI = HWLOC_OBJ_BRIDGE_PCI

OBJ_OSDEV_BLOCK = HWLOC_OBJ_OSDEV_BLOCK
OBJ_OSDEV_GPU = HWLOC_OBJ_OSDEV_GPU
OBJ_OSDEV_NETWORK = HWLOC_OBJ_OSDEV_NETWORK
OBJ_OSDEV_OPENFABRICS = HWLOC_OBJ_OSDEV_OPENFABRICS
OBJ_OSDEV_DMA = HWLOC_OBJ_OSDEV_DMA
OBJ_OSDEV_COPROC = HWLOC_OBJ_OSDEV_COPROC

TYPE_UNORDERED = HWLOC_TYPE_UNORDERED

TOPOLOGY_FLAG_WHOLE_SYSTEM = HWLOC_TOPOLOGY_FLAG_WHOLE_SYSTEM
TOPOLOGY_FLAG_IS_THISSYSTEM = HWLOC_TOPOLOGY_FLAG_IS_THISSYSTEM
TOPOLOGY_FLAG_IO_DEVICES = HWLOC_TOPOLOGY_FLAG_IO_DEVICES
TOPOLOGY_FLAG_IO_BRIDGES = HWLOC_TOPOLOGY_FLAG_IO_BRIDGES
TOPOLOGY_FLAG_WHOLE_IO = HWLOC_TOPOLOGY_FLAG_WHOLE_IO
TOPOLOGY_FLAG_ICACHES = HWLOC_TOPOLOGY_FLAG_ICACHES

RESTRICT_FLAG_ADAPT_DISTANCES = HWLOC_RESTRICT_FLAG_ADAPT_DISTANCES
RESTRICT_FLAG_ADAPT_MISC = HWLOC_RESTRICT_FLAG_ADAPT_MISC
RESTRICT_FLAG_ADAPT_IO = HWLOC_RESTRICT_FLAG_ADAPT_IO

TYPE_DEPTH_UNKNOWN = HWLOC_TYPE_DEPTH_UNKNOWN
TYPE_DEPTH_MULTIPLE = HWLOC_TYPE_DEPTH_MULTIPLE
TYPE_DEPTH_BRIDGE = HWLOC_TYPE_DEPTH_BRIDGE
TYPE_DEPTH_PCI_DEVICE = HWLOC_TYPE_DEPTH_PCI_DEVICE
TYPE_DEPTH_OS_DEVICE = HWLOC_TYPE_DEPTH_OS_DEVICE

CPUBIND_PROCESS = HWLOC_CPUBIND_PROCESS
CPUBIND_THREAD = HWLOC_CPUBIND_THREAD
CPUBIND_STRICT = HWLOC_CPUBIND_STRICT
CPUBIND_NOMEMBIND = HWLOC_CPUBIND_NOMEMBIND

MEMBIND_DEFAULT = HWLOC_MEMBIND_DEFAULT
MEMBIND_FIRSTTOUCH = HWLOC_MEMBIND_FIRSTTOUCH
MEMBIND_BIND = HWLOC_MEMBIND_BIND
MEMBIND_INTERLEAVE = HWLOC_MEMBIND_INTERLEAVE
MEMBIND_REPLICATE = HWLOC_MEMBIND_REPLICATE
MEMBIND_NEXTTOUCH = HWLOC_MEMBIND_NEXTTOUCH
MEMBIND_MIXED = HWLOC_MEMBIND_MIXED

MEMBIND_PROCESS = HWLOC_MEMBIND_PROCESS
MEMBIND_THREAD = HWLOC_MEMBIND_THREAD
MEMBIND_STRICT = HWLOC_MEMBIND_STRICT
MEMBIND_MIGRATE = HWLOC_MEMBIND_MIGRATE
MEMBIND_NOCPUBIND = HWLOC_MEMBIND_NOCPUBIND
MEMBIND_BYNODESET = HWLOC_MEMBIND_BYNODESET

TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_EXTENDED_TYPES = HWLOC_TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_EXTENDED_TYPES
TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_ATTRS = HWLOC_TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_ATTRS

TOPOLOGY_DIFF_OBJ_ATTR_SIZE = HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_SIZE
TOPOLOGY_DIFF_OBJ_ATTR_NAME = HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_NAME
TOPOLOGY_DIFF_OBJ_ATTR_INFO = HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_INFO
TOPOLOGY_DIFF_OBJ_ATTR = HWLOC_TOPOLOGY_DIFF_OBJ_ATTR
TOPOLOGY_DIFF_TOO_COMPLEX = HWLOC_TOPOLOGY_DIFF_TOO_COMPLEX

TOPOLOGY_DIFF_APPLY_REVERSE = HWLOC_TOPOLOGY_DIFF_APPLY_REVERSE

####
# CUDA Driver API Specific Functions
####
#
#
#  **  I can't develop these interfaces without the proprietary NVIDIA libraries **
#
#
#ctypedef int CUdevice
#
#cdef extern from "hwloc/cuda.h":
#	int hwloc_cuda_get_device_pci_ids(hwloc_topology_t topology, CUdevice cu#device,
#									  int *d#omain, int *bus, int *dev)
#	int hwloc_cuda_get_device_cpuset(hwloc_topology_t topology, CUdevice cud#evice,
#									 hwloc_c#puset_t set1)
#	hwloc_obj_t hwloc_cuda_get_device_pcidev(hwloc_topology_t topology,
#										#	 CUdevice cudevice)
#	hwloc_obj_t hwloc_cuda_get_device_osdev(hwloc_topology_t topology,
#										#	CUdevice cudevice)
#	hwloc_obj_t hwloc_cuda_get_device_osdev_by_index(hwloc_topology_t topolo#gy,
#										#			 unsigned idx)

#cdef extern from "hwloc/cudart.h":
#	int hwloc_cudart_get_device_pci_ids(hwloc_topology_t topology, int idx,
#										#int *domain, int *bus, int *dev)
#	int hwloc_cudart_get_device_cpuset(hwloc_topology_t topology, int idx,
#									   hwloc#_cpuset_t set1)
#	hwloc_obj_t hwloc_cudart_get_device_pcidev(hwloc_topology_t topology, in#t idx)
#	hwloc_obj_t hwloc_cudart_get_device_osdev_by_index(hwloc_topology_t topo#logy,
#										#			   unsigned idx)

IF WITH_x86_64:
	####
	# Linux libnuma interaction
	####
	cdef extern from "numa.h":
		cdef struct bitmask:
			pass

	cdef extern from "hwloc/linux-libnuma.h":
		# Helpers for manipulating Linux libnuma unsigned long masks
		int hwloc_cpuset_to_linux_libnuma_ulongs(hwloc_topology_t topology,
												 hwloc_const_cpuset_t cpuset,
												 unsigned long* mask,
												 unsigned long* maxnode)
		int hwloc_nodeset_to_linux_libnuma_ulongs(hwloc_topology_t topology,
												  hwloc_const_nodeset_t nodeset,
												  unsigned long* mask,
												  unsigned long* maxnode)
		int hwloc_cpuset_from_linux_libnuma_ulongs(hwloc_topology_t topology,
												   hwloc_cpuset_t cpuset,
												   const unsigned long* mask,
												   unsigned long maxnode)
		int hwloc_nodeset_from_linux_libnuma_ulongs(hwloc_topology_t topology,
													hwloc_nodeset_t nodeset,
													const unsigned long* mask,
													unsigned long maxnode)
		# Helpers for manipulating Linux libnuma bitmask
		bitmask* hwloc_cpuset_to_linux_libnuma_bitmask(hwloc_topology_t topology,
													   hwloc_const_cpuset_t cpuset)
		bitmask* hwloc_nodeset_to_linux_libnuma_bitmask(hwloc_topology_t topology,
  													  hwloc_const_nodeset_t nodeset)
		int hwloc_cpuset_from_linux_libnuma_bitmask(hwloc_topology_t topology,
													hwloc_cpuset_t cpuset,
													const bitmask* bitmask)
		int hwloc_nodeset_from_linux_libnuma_bitmask(hwloc_topology_t topology,
													 hwloc_nodeset_t nodeset,
													 const bitmask* bitmask)
#ENDIF

####
# Interoperability with Intel Xeon Phi (MIC)
####
cdef extern from "hwloc/intel-mic.h":
	int hwloc_intel_mic_get_device_cpuset(hwloc_topology_t topology, int idx,
										  hwloc_cpuset_t set1)
	hwloc_obj_t hwloc_intel_mic_get_device_osdev_by_index(hwloc_topology_t topology,
														  unsigned idx)

####
# NVIDIA Management Library Specific Functions
####
# don't have /usr/include/nvml.h
#cdef extern from "hwloc/nvml.h":
#	int hwloc_nvml_get_device_cpuset(hwloc_topology_t topology,
#									 nvmlDevice_t device, hwloc_cpuset_t set1)
#	hwloc_obj_t hwloc_nvml_get_device_osdev_by_index(hwloc_topology_t topology,
#													 unsigned idx)
#	hwloc_obj_t hwloc_nvml_get_device_osdev(hwloc_topology_t topology,
#											nvmlDevice_t device)

IF WITH_x86_64:
####
# Interoperability with OpenFabrics
####
#
	cdef extern from "hwloc/openfabrics-verbs.h":
# need python bindings for OF verbs
#		int hwloc_ibv_get_device_cpuset(hwloc_topology_t topology,
#										ibv_device *ibdev, hwloc_cpuset_t set1)
		hwloc_obj_t hwloc_ibv_get_device_osdev_by_name(hwloc_topology_t topology,
													   const char *ibname)
# need Python bindings for OF verbs
#		hwloc_obj_t hwloc_ibv_get_device_osdev(hwloc_topology_t topology,
#											   struct ibv_device *ibdev)
#ENDIF


cdef class __ptr(object):
	cdef const void* _pointer
	def __cinit__(self):
		self._pointer = NULL
	cdef const void* get(self):
		return self._pointer
	cdef set(self, const void* v):
			self._pointer = v
	def __richcmp__(x, y, op):
		if isinstance(x, __ptr) and isinstance(y, __ptr) and op == 2:
			return <unsigned long>(<__ptr>x).get() == <unsigned long>(<__ptr>y).get()
		else:
			return NotImplemented

__userdata_export_callbacks = {}
__userdata_import_callbacks = {}

cdef void __userdata_export_callback(void* reserved, hwloc_topology_t topology, hwloc_obj_t obj):
	t = __topology_handle()
	t.set(topology)
	cb = __userdata_export_callbacks[<unsigned long>t.ptr()]
	assert cb is not None
	cb(int(<unsigned long>reserved), t, __omake(obj))

cdef void __userdata_import_callback(hwloc_topology_t topology, hwloc_obj_t  obj, const char* name, const void* buf, size_t length):
	t = __topology_handle()
	t.set(topology)
	cb = __userdata_import_callbacks[<unsigned long>t.ptr()]
	assert cb is not None
	cdef char* p = <char*>buf
	b = p[:length].decode('utf8')
	n = name.decode('utf8')
	cb(t, __omake(obj), n, str(b))

def __checkneg1(int value):
	if value == -1:
		raise OSError(CErrno, CStrerror(CErrno))
	return value

cdef const void* __checknull(const void* p) except NULL:
	if p == NULL:
		raise OSError(CErrno, CStrerror(CErrno))
	return p

cdef const void* __checknone(const void* p) except NULL:
	if p == NULL:
		raise NULLError()
	return p


####
# hwlocality_bitmap The bitmap API
####
cdef class __bitmap_ptr(__ptr):
	cdef hwloc_bitmap_t ptr(self):
		return <hwloc_bitmap_t>self.get()

cdef class volatile_bitmap_ptr(__bitmap_ptr):
	def __dealloc__(self):
		if self._pointer != NULL:
			hwloc_bitmap_free(<hwloc_bitmap_t>self._pointer)

cdef volatile_bitmap_ptr __bnew(hwloc_bitmap_t bitmap):
	b = volatile_bitmap_ptr()
	b.set(__checknull(bitmap))
	return b

cdef volatile_bitmap_ptr __bmake(hwloc_const_bitmap_t bitmap):
	__checknone(bitmap)
	return __bnew(hwloc_bitmap_dup(bitmap))

cdef volatile_bitmap_ptr __bitmap_alloc():
	return __bnew(hwloc_bitmap_alloc())

def bitmap_alloc():
	return __bitmap_alloc()

cdef volatile_bitmap_ptr __bitmap_alloc_full():
	return __bnew(hwloc_bitmap_alloc_full())

def bitmap_alloc_full():
	return __bitmap_alloc_full()

cdef volatile_bitmap_ptr __bitmap_dup(__bitmap_ptr bitmap):
	return __bnew(hwloc_bitmap_dup(bitmap.ptr()))

def bitmap_dup(bitmap):
	return __bitmap_dup(bitmap)

def bitmap_copy(__bitmap_ptr dst, __bitmap_ptr src):
	hwloc_bitmap_copy(dst.ptr(), src.ptr())

# no reason for bitmap_snprintf

def bitmap_asprintf(__bitmap_ptr bitmap):
	cdef char* p
	__checkneg1(hwloc_bitmap_asprintf(&p, bitmap.ptr()))
	b = p.decode('utf8')
	CFree(p)
	return str(b)

def bitmap_sscanf(__bitmap_ptr bitmap, string):
	s = _utfate(string)
	if hwloc_bitmap_sscanf(bitmap.ptr(), s) == -1:
		raise ArgError('hwloc_bitmap_sscanf: ' + string)

# no reason for bitmap_list_snprintf

def bitmap_list_asprintf(__bitmap_ptr bitmap):
	cdef char* p
	__checkneg1(hwloc_bitmap_list_asprintf(&p, bitmap.ptr()))
	b = p.decode('utf8')
	CFree(p)
	return str(b)

def bitmap_list_sscanf(__bitmap_ptr bitmap, string):
	s = _utfate(string)
	if hwloc_bitmap_list_sscanf(bitmap.ptr(), s) == -1:
		raise ArgError('hwloc_bitmap_list_sscanf: ' + string)

# no reason for bitmap_taskset_snprintf

def bitmap_taskset_asprintf(__bitmap_ptr bitmap):
	cdef char* p
	__checkneg1(hwloc_bitmap_taskset_asprintf(&p, bitmap.ptr()))
	b = p.decode('utf8')
	CFree(p)
	return str(b)

def bitmap_taskset_sscanf(__bitmap_ptr bitmap, string):
	s = _utfate(string)
	if hwloc_bitmap_taskset_sscanf(bitmap.ptr(), s) == -1:
		raise ArgError('hwloc_bitmap_taskset_sscanf: ' + string)

def bitmap_zero(__bitmap_ptr bitmap):
	hwloc_bitmap_zero(bitmap.ptr())

def bitmap_fill(__bitmap_ptr bitmap):
	hwloc_bitmap_fill(bitmap.ptr())

def bitmap_only(__bitmap_ptr bitmap, unsigned id1):
	hwloc_bitmap_only(bitmap.ptr(), id1)

def bitmap_allbut(__bitmap_ptr bitmap, unsigned id1):
	hwloc_bitmap_allbut(bitmap.ptr(), id1)

# bitmap_from_ulong is bitmap_from_ith_ulong(,1,)

def bitmap_from_ith_ulong(__bitmap_ptr bitmap, unsigned i, unsigned long mask):
	hwloc_bitmap_from_ith_ulong(bitmap.ptr(), i, mask)

def bitmap_set(__bitmap_ptr bitmap, id1):
	hwloc_bitmap_set(bitmap.ptr(), int(id1))

def bitmap_set_range(__bitmap_ptr bitmap, unsigned begin, int end):
	hwloc_bitmap_set_range(bitmap.ptr(), begin, end)

def bitmap_set_ith_ulong(__bitmap_ptr bitmap, unsigned i, unsigned mask):
	hwloc_bitmap_set_ith_ulong(bitmap.ptr(), i, mask)

def bitmap_clr(__bitmap_ptr bitmap, unsigned id1):
	hwloc_bitmap_clr(bitmap.ptr(), id1)

def bitmap_clr_range(__bitmap_ptr bitmap, unsigned begin, int end):
	hwloc_bitmap_clr_range(bitmap.ptr(), begin, end)

def bitmap_singlify(__bitmap_ptr bitmap):
	hwloc_bitmap_singlify(bitmap.ptr())

# bitmap_to_ulong is bitmap_to_ith_ulong(,1)

def bitmap_to_ith_ulong(__bitmap_ptr bitmap, unsigned i):
	return int(hwloc_bitmap_to_ith_ulong(bitmap.ptr(), i))

def bitmap_isset(__bitmap_ptr bitmap, unsigned id1):
	return int(hwloc_bitmap_isset(bitmap.ptr(), id1))

def bitmap_iszero(__bitmap_ptr bitmap):
	return int(hwloc_bitmap_iszero(bitmap.ptr()))

def bitmap_isfull(__bitmap_ptr bitmap):
	return int(hwloc_bitmap_isfull(bitmap.ptr()))

def bitmap_first(__bitmap_ptr bitmap):
	return int(hwloc_bitmap_first(bitmap.ptr()))

def bitmap_next(__bitmap_ptr bitmap, int prev):
	return int(hwloc_bitmap_next(bitmap.ptr(), prev))

def bitmap_last(__bitmap_ptr bitmap):
	return int(hwloc_bitmap_last(bitmap.ptr()))

def bitmap_weight(__bitmap_ptr bitmap):
	return int(hwloc_bitmap_weight(bitmap.ptr()))

def bitmap_or(__bitmap_ptr res, __bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	hwloc_bitmap_or(res.ptr(), bitmap1.ptr(), bitmap2.ptr())

def bitmap_and(__bitmap_ptr res, __bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	hwloc_bitmap_and(res.ptr(), bitmap1.ptr(), bitmap2.ptr())

def bitmap_andnot(__bitmap_ptr res, __bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	hwloc_bitmap_andnot(res.ptr(), bitmap1.ptr(), bitmap2.ptr())

def bitmap_xor(__bitmap_ptr res, __bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	hwloc_bitmap_xor(res.ptr(), bitmap1.ptr(), bitmap2.ptr())

def bitmap_not(__bitmap_ptr res, __bitmap_ptr bitmap):
	hwloc_bitmap_not(res.ptr(), bitmap.ptr())

def bitmap_intersects(__bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	return int(hwloc_bitmap_intersects(bitmap1.ptr(), bitmap2.ptr()))

def bitmap_isincluded(__bitmap_ptr sub_bitmap, __bitmap_ptr super_bitmap):
	return int(hwloc_bitmap_isincluded(sub_bitmap.ptr(), super_bitmap.ptr()))

def bitmap_isequal(__bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	return int(hwloc_bitmap_isequal(bitmap1.ptr(), bitmap2.ptr()))

def bitmap_compare_first(__bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	return int(hwloc_bitmap_compare_first(bitmap1.ptr(), bitmap2.ptr()))

def bitmap_compare(__bitmap_ptr bitmap1, __bitmap_ptr bitmap2):
	return int(hwloc_bitmap_compare(bitmap1.ptr(), bitmap2.ptr()))

####
# API version
####
def get_api_version():
	return int(hwloc_get_api_version())

cdef class tds_ptr(__ptr):
	property pu:
		def __get__(self):
			return int((<hwloc_topology_discovery_support*>self.get()).pu)

cdef class cbs_ptr(__ptr):
	cdef hwloc_topology_cpubind_support* ptr(self):
		return <hwloc_topology_cpubind_support*>self.get()

	property set_thisproc_cpubind:
		def __get__(self):
			return int(self.ptr().set_thisproc_cpubind)

	property get_thisproc_cpubind:
		def __get__(self):
			return int(self.ptr().get_thisproc_cpubind)

	property set_proc_cpubind:
		def __get__(self):
			return int(self.ptr().set_proc_cpubind)

	property get_proc_cpubind:
		def __get__(self):
			return int(self.ptr().get_proc_cpubind)

	property set_thisthread_cpubind:
		def __get__(self):
			return int(self.ptr().set_thisthread_cpubind)

	property get_thisthread_cpubind:
		def __get__(self):
			return int(self.ptr().get_thisthread_cpubind)

	property set_thread_cpubind:
		def __get__(self):
			return int(self.ptr().set_thread_cpubind)

	property get_thread_cpubind:
		def __get__(self):
			return int(self.ptr().get_thread_cpubind)

	property get_thisproc_last_cpu_location:
		def __get__(self):
			return int(self.ptr().get_thisproc_last_cpu_location)

	property get_proc_last_cpu_location:
		def __get__(self):
			return int(self.ptr().get_proc_last_cpu_location)

	property get_thisthread_last_cpu_location:
		def __get__(self):
			return int(self.ptr().get_thisthread_last_cpu_location)

cdef class mbs_ptr(__ptr):
	cdef hwloc_topology_membind_support* ptr(self):
		return <hwloc_topology_membind_support*>self.get()

	property set_thisproc_membind:
		def __get__(self):
			return int(self.ptr().set_thisproc_membind)

	property get_thisproc_membind:
		def __get__(self):
			return int(self.ptr().get_thisproc_membind)

	property set_proc_membind:
		def __get__(self):
			return int(self.ptr().set_proc_membind)

	property get_proc_membind:
		def __get__(self):
			return int(self.ptr().get_proc_membind)

	property set_thisthread_membind:
		def __get__(self):
			return int(self.ptr().set_thisthread_membind)

	property get_thisthread_membind:
		def __get__(self):
			return int(self.ptr().get_thisthread_membind)

	property set_area_membind:
		def __get__(self):
			return int(self.ptr().set_area_membind)

	property get_area_membind:
		def __get__(self):
			return int(self.ptr().get_area_membind)

	property alloc_membind:
		def __get__(self):
			return int(self.ptr().alloc_membind)

	property firsttouch_membind:
		def __get__(self):
			return int(self.ptr().firsttouch_membind)

	property bind_membind:
		def __get__(self):
			return int(self.ptr().bind_membind)

	property interleave_membind:
		def __get__(self):
			return int(self.ptr().interleave_membind)

	property replicate_membind:
		def __get__(self):
			return int(self.ptr().replicate_membind)

	property nexttouch_membind:
		def __get__(self):
			return int(self.ptr().nexttouch_membind)

	property migrate_membind:
		def __get__(self):
			return int(self.ptr().migrate_membind)

	property get_area_memlocation:
		def __get__(self):
			return int(self.ptr().get_area_memlocation)

cdef class ts_ptr(__ptr):
	cdef hwloc_topology_support* ptr(self):
		return <hwloc_topology_support*>self.get()

	property discovery:
		def __get__(self):
			p = tds_ptr()
			p.set(self.ptr().discovery)
			return p

	property cpubind:
		def __get__(self):
			p = cbs_ptr()
			p.set(self.ptr().cpubind)
			return p

	property membind:
		def __get__(self):
			p = mbs_ptr()
			p.set(self.ptr().membind)
			return p

cdef class ompt_ptr(__ptr):
	cdef hwloc_obj_memory_page_type_s* ptr(self):
		return <hwloc_obj_memory_page_type_s*>self.get()

	property size:
		def __get__(self):
			return int(self.ptr().size)

	property count:
		def __get__(self):
			return int(self.ptr().count)

cdef class memory_ptr(__ptr):
	cdef hwloc_obj_memory_s* ptr(self):
		return <hwloc_obj_memory_s*>self.get()

	property total_memory:
		def __get__(self):
			return int(self.ptr().total_memory)

	property local_memory:
		def __get__(self):
			return int(self.ptr().local_memory)
		def __set__(self, uint64_t value):
			self.ptr().local_memory = value

	property page_types_len:
		def __get__(self):
			return int(self.ptr().page_types_len)

	property page_types:
		def __get__(self):
			cdef size_t i
			for i in range(self.page_types_len):
				o = ompt_ptr()
				o.set(&self.ptr().page_types[i])
				yield o

cdef class cattr_ptr(__ptr):
	cdef hwloc_cache_attr_s* ptr(self):
		return <hwloc_cache_attr_s*>self.get()

	property size:
		def __get__(self):
			return int(self.ptr().size)

	property depth:
		def __get__(self):
			return int(self.ptr().depth)

	property linesize:
		def __get__(self):
			return int(self.ptr().linesize)

	property associativity:
		def __get__(self):
			return int(self.ptr().associativity)

	property type:
		def __get__(self):
			return int(<int>self.ptr().type)

cdef class gattr_ptr(__ptr):
	cdef hwloc_group_attr_s* ptr(self):
		return <hwloc_group_attr_s*>self.get()

	property depth:
		def __get__(self):
			return int(self.ptr().depth)

cdef class pattr_ptr(__ptr):
	cdef hwloc_pcidev_attr_s* ptr(self):
		return <hwloc_pcidev_attr_s*>self.get()

	property domain:
		def __get__(self):
			return int(self.ptr().domain)

	property bus:
		def __get__(self):
			return int(self.ptr().bus)

	property dev:
		def __get__(self):
			return int(self.ptr().dev)

	property func:
		def __get__(self):
			return int(self.ptr().func)

	property class_id:
		def __get__(self):
			return int(self.ptr().class_id)

	property vendor_id:
		def __get__(self):
			return int(self.ptr().vendor_id)

	property device_id:
		def __get__(self):
			return int(self.ptr().device_id)

	property subvendor_id:
		def __get__(self):
			return int(self.ptr().subvendor_id)

	property subdevice_id:
		def __get__(self):
			return int(self.ptr().subdevice_id)

	property revision:
		def __get__(self):
			return int(self.ptr().revision)

	property linkspeed:
		def __get__(self):
			return float(self.ptr().linkspeed)

cdef class bups_ptr(__ptr):
	property pci:
		def __get__(self):
			p = pattr_ptr()
			p.set(&(<ba_upstream*>self.get()).pci)
			return p

cdef class bdowns_s_ptr(__ptr):
	cdef ba_ds_pci* ptr(self):
		return <ba_ds_pci*>self.get()

	property domain:
		def __get__(self):
			return int(self.ptr().domain)

	property secondary_bus:
		def __get__(self):
			return int(self.ptr().secondary_bus)

	property subordinate_bus:
		def __get__(self):
			return int(self.ptr().subordinate_bus)

cdef class bd_pci_ptr(__ptr):
	property pci:
		def __get__(self):
			p = bdowns_s_ptr()
			p.set(self.get())
			return p

cdef class battr_ptr(__ptr):
	cdef hwloc_bridge_attr_s* ptr(self):
		return <hwloc_bridge_attr_s*>self.get()

	property upstream:
		def __get__(self):
			p = bups_ptr()
			p.set(&self.ptr().upstream)
			return p

	property upstream_type:
		def __get__(self):
			return int(self.ptr().upstream_type)

	property downstream:
		def __get__(self):
			p = bd_pci_ptr()
			p.set(&self.ptr().downstream)
			return p

	property downstream_type:
		def __get__(self):
			return int(self.ptr().downstream_type)

	property depth:
		def __get__(self):
			return int(<int>self.ptr().depth)

cdef class oattr_ptr(__ptr):
	property type:
		def __get__(self):
			return int((<hwloc_osdev_attr_s*>self.get()).type)

cdef class attr_ptr(__ptr):
	cdef hwloc_obj_attr_u* ptr(self):
		return <hwloc_obj_attr_u*>self.get()

	property cache:
		def __get__(self):
			p = cattr_ptr()
			p.set(&self.ptr().cache)
			return p

	property group:
		def __get__(self):
			p = gattr_ptr()
			p.set(&self.ptr().group)
			return p

	property pcidev:
		def __get__(self):
			p = pattr_ptr()
			p.set(&self.ptr().pcidev)
			return p

	property bridge:
		def __get__(self):
			p = battr_ptr()
			p.set(&self.ptr().bridge)
			return p

	property osdev:
		def __get__(self):
			p = oattr_ptr()
			p.set(&self.ptr().osdev)
			return p

cdef class distances_ptr(__ptr):
	cdef hwloc_distances_s* ptr(self):
		return <hwloc_distances_s*>self.get()

	property relative_depth:
		def __get__(self):
			return int(<int>self.ptr().relative_depth)

	property nbobjs:
		def __get__(self):
			return int(self.ptr().nbobjs)

	property latency:
		def __get__(self):
			cdef size_t i
			return tuple([float(self.ptr().latency[i]) for i in range(self.nbobjs*self.nbobjs)])

	property latency_max:
		def __get__(self):
			return float(self.ptr().latency_max)

	property latency_base:
		def __get__(self):
			return float(self.ptr().latency_base)

cdef class info_ptr(__ptr):
	cdef hwloc_obj_info_s* ptr(self):
		return <hwloc_obj_info_s*>self.get()

	property name:
		def __get__(self):
			return <bytes> self.ptr().name

	property value:
		def __get__(self):
			return <bytes> self.ptr().value

cdef obj_ptr __omake(const void* v):
	p = obj_ptr()
	p.set(__checknone(v))
	return p

cdef hwloc_obj_t __oget(obj_ptr instance):
	if instance is None:
		return <hwloc_obj_t>NULL
	return instance.ptr()

####
# Topology Object types
####
cdef class obj_ptr(__ptr):
	cdef hwloc_obj_t ptr(self):
		return <hwloc_obj_t>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)
	property os_index:
		def __get__(self):
			# this is kind of hacky but the library returns -1 when the index
			# is unknown or not applicable. We have to convert it to the right
			# size signed value so we can compare it against -1 later.
			return int(<int>self.ptr().os_index)
	property name:
		def __get__(self):
			if self.ptr().name == NULL:
				return None
			return <bytes>self.ptr().name
	property memory:
		def __get__(self):
			p = memory_ptr()
			p.set(&self.ptr().memory)
			return p
	property attr:
		def __get__(self):
			p = attr_ptr()
			p.set(__checknone(self.ptr().attr))
			return p
	property depth:
		def __get__(self):
			return int(<int>self.ptr().depth)
	property logical_index:
		def __get__(self):
			return int(self.ptr().logical_index)
	property os_level:
		def __get__(self):
			return int(self.ptr().os_level)
	property next_cousin:
		def __get__(self):
			return __omake(self.ptr().next_cousin)
	property prev_cousin:
		def __get__(self):
			return __omake(self.ptr().prev_cousin)
	property parent:
		def __get__(self):
			return __omake(self.ptr().parent)
	property sibling_rank:
		def __get__(self):
			return int(self.ptr().sibling_rank)
	property next_sibling:
		def __get__(self):
			return __omake(self.ptr().next_sibling)
	property prev_sibling:
		def __get__(self):
			return __omake(self.ptr().prev_sibling)
	property arity:
		def __get__(self):
			return int(self.ptr().arity)
	property children:
		def __get__(self):
			l = []
			cdef hwloc_obj** p = self.ptr().children
			cdef size_t i
			for i in range(self.arity):
				l.append(__omake(p[i]))
			return tuple(l)
	property first_child:
		def __get__(self):
			return __omake(self.ptr().first_child)
	property last_child:
		def __get__(self):
			return __omake(self.ptr().last_child)
	property userdata:
		def __get__(self):
			return int(<unsigned long>self.ptr().userdata)
		def __set__(self, unsigned long data):
			self.ptr().userdata = <void*>data
	property cpuset:
		def __get__(self):
			return __bmake(self.ptr().cpuset)
	property complete_cpuset:
		def __get__(self):
			return __bmake(self.ptr().complete_cpuset)
	property online_cpuset:
		def __get__(self):
			return __bmake(self.ptr().online_cpuset)
	property allowed_cpuset:
		def __get__(self):
			return __bmake(self.ptr().allowed_cpuset)
	property nodeset:
		def __get__(self):
			return __bmake(self.ptr().nodeset)
	property complete_nodeset:
		def __get__(self):
			return __bmake(self.ptr().complete_nodeset)
	property allowed_nodeset:
		def __get__(self):
			return __bmake(self.ptr().allowed_nodeset)
	property distances:
		def __get__(self):
			l = []
			cdef hwloc_distances_s** p = self.ptr().distances
			cdef size_t i
			for i in range(self.distances_count):
				d = distances_ptr()
				d.set(p[i])
				l.append(d)
			return tuple(l)
	property distances_count:
		def __get__(self):
			return int(self.ptr().distances_count)
	property infos:
		def __get__(self):
			l = []
			cdef hwloc_obj_info_s* p = self.ptr().infos
			cdef size_t i
			for i in range(self.infos_count):
				d = info_ptr()
				d.set(&p[i])
				l.append(d)
			return tuple(l)
	property infos_count:
		def __get__(self):
			return int(self.ptr().infos_count)
	property symmetric_subtree:
		def __get__(self):
			return int(self.ptr().symmetric_subtree)


def compare_types(hwloc_obj_type_t type1, hwloc_obj_type_t type2):
	return int(hwloc_compare_types(type1, type2))

####
# Create and Destroy Topologies
####
cdef class __topology_handle(__ptr):
	cdef hwloc_topology_t ptr(self):
		return <hwloc_topology_t>self.get()

cdef class topology_ptr(__topology_handle):
	def __init__(self, init=True):
		# work around a hwloc bug
		import os
		if 'HWLOC_PLUGINS_VERBOSE' not in os.environ:
			os.environ['HWLOC_PLUGINS_VERBOSE'] = '0'
		self._pointer = NULL
		if init:
			__checkneg1(hwloc_topology_init(<hwloc_topology_t*>&self._pointer))
		__userdata_export_callbacks[<unsigned long>self._pointer] = None
		__userdata_import_callbacks[<unsigned long>self._pointer] = None
	def __dealloc__(self):
		try:
			del __userdata_export_callbacks[<unsigned long>self._pointer]
		except:
			pass
		try:
			del __userdata_import_callbacks[<unsigned long>self._pointer]
		except:
			pass
		if self._pointer != NULL:
			hwloc_topology_destroy(self.ptr())


cdef hwloc_topology_t __tget(__topology_handle instance):
	if instance is None:
		return <hwloc_topology_t>NULL
	return <hwloc_topology_t>instance.get()

def topology_load(__topology_handle topology):
	__checkneg1(hwloc_topology_load(topology.ptr()))

def topology_check(__topology_handle topology):
	hwloc_topology_check(topology.ptr())

####
# Configure Topology Detection
####
def topology_ignore_type(__topology_handle topology, hwloc_obj_type_t type1):
	__checkneg1(hwloc_topology_ignore_type(topology.ptr(), type1))

def topology_ignore_type_keep_structure(__topology_handle topology, hwloc_obj_type_t type1):
	__checkneg1(hwloc_topology_ignore_type_keep_structure(topology.ptr(), type1))

def topology_ignore_all_keep_structure(__topology_handle topology):
	hwloc_topology_ignore_all_keep_structure(topology.ptr())

def topology_set_flags(__topology_handle topology, unsigned long flags):
	hwloc_topology_set_flags(topology.ptr(), flags)

def topology_set_pid(__topology_handle topology, hwloc_pid_t pid):
	__checkneg1(hwloc_topology_set_pid(topology.ptr(), pid))

def topology_set_fsroot(__topology_handle topology, fsroot_path):
	fsroot_path = _utfate(fsroot_path)
	__checkneg1(hwloc_topology_set_fsroot(topology.ptr(), fsroot_path))

def topology_set_synthetic(__topology_handle topology, description):
	description = _utfate(description)
	__checkneg1(hwloc_topology_set_synthetic(topology.ptr(), description))

def topology_set_xml(__topology_handle topology, xmlpath):
	xmlpath = _utfate(xmlpath)
	__checkneg1(hwloc_topology_set_xml(topology.ptr(), xmlpath))

def topology_set_xmlbuffer(__topology_handle topology, buffer1):
	buffer1 = _utfate(buffer1)
	__checkneg1(hwloc_topology_set_xmlbuffer(topology.ptr(), buffer1, len(buffer1)))

def topology_set_custom(__topology_handle topology):
	__checkneg1(hwloc_topology_set_custom(topology.ptr()))

def topology_set_distance_matrix(__topology_handle topology, hwloc_obj_type_t type1, os_index,
								 distances):
	cdef int nbobjs = len(os_index)
	if nbobjs * nbobjs != len(distances):
		raise ArgError('distances must be a square of indexes')
	cdef unsigned* indexp
	cdef float* distancep
	# The library routine insists that the array pointers be NULL
	# if the nbobjs is zero.
	if nbobjs == 0:
		indexp = NULL
		distancep = NULL
	else:
		indexp = <unsigned*>CMalloc(sizeof(unsigned) * nbobjs)
		if indexp == NULL:
			raise OSError(CErrno, CStrerror(CErrno))
		distancep = <float*>CMalloc(sizeof(float) * nbobjs * nbobjs)
		if distancep == NULL:
			raise OSError(CErrno, CStrerror(CErrno))
		i = 0
		for j in os_index:
			indexp[i] = <int>j
			i += 1
		i = 0
		for j in distances:
			distancep[i] = float(j)
			i += 1
	try:
		if hwloc_topology_set_distance_matrix(topology.ptr(),
											  type1,
											  nbobjs,
											  indexp,
											  distancep) == -1:
			raise ArgError('hwloc_topology_set_distance_matrix')
	finally:
		CFree(indexp)
		CFree(distancep)

def topology_is_thissystem(__topology_handle topology):
	return int(hwloc_topology_is_thissystem(topology.ptr()))

def topology_get_support(__topology_handle topology):
	s = ts_ptr()
	s.set(<void*>hwloc_topology_get_support(topology.ptr()))
	return s

# There is really no point in implementing these bindings. If we just store and
# return the value in our topology object instance, we can even make the
# userdata a Python object.
def topology_set_userdata(__topology_handle topology, userdata):
	hwloc_topology_set_userdata(topology.ptr(), <const void*>userdata)

def topology_get_userdata(__topology_handle topology):
	return int(<unsigned long>hwloc_topology_get_userdata(topology.ptr()))

####
# Object levels, depths and types
####
def topology_get_depth(__topology_handle topology):
	return int(hwloc_topology_get_depth(topology.ptr()))

def get_type_depth(__topology_handle topology, hwloc_obj_type_t type1):
	return int(hwloc_get_type_depth(topology.ptr(), type1))

def get_type_or_below_depth(__topology_handle topology, hwloc_obj_type_t type1):
	return int(hwloc_get_type_or_below_depth(topology.ptr(), type1))

def get_type_or_above_depth(__topology_handle topology, hwloc_obj_type_t type1):
	return int(hwloc_get_type_or_above_depth(topology.ptr(), type1))

def get_depth_type(__topology_handle topology, int depth):
	cdef hwloc_obj_type_t t
	t = hwloc_get_depth_type(topology.ptr(), depth)
	if <int>t == -1:
		raise ArgError('hwloc_get_depth_type')
	return t

def get_nbobjs_by_depth(__topology_handle topology, int depth):
	return int(hwloc_get_nbobjs_by_depth(topology.ptr(), depth))

def get_nbobjs_by_type(__topology_handle topology, hwloc_obj_type_t type1):
	return int(hwloc_get_nbobjs_by_type(topology.ptr(), type1))

def get_root_obj(__topology_handle topology):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_root_obj(topology.ptr())))
	return p

def get_obj_by_depth(__topology_handle topology, int depth, unsigned idx):
	return __omake(hwloc_get_obj_by_depth(topology.ptr(), depth, idx))

def get_obj_by_type(__topology_handle topology, hwloc_obj_type_t type1, unsigned idx):
	return __omake(hwloc_get_obj_by_type(topology.ptr(), type1, idx))

def get_next_obj_by_depth(__topology_handle topology, int depth, obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_obj_by_depth(topology.ptr(), depth,
												  __oget(prev))))
	return p

def get_next_obj_by_type(__topology_handle topology, hwloc_obj_type_t type1,
						 obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_obj_by_type(topology.ptr(), type1,
												 __oget(prev))))
	return p

def topology_get_flags(__topology_handle topology):
	return int(hwloc_topology_get_flags(topology.ptr()))

####
# Object Type, Sets and Attributes as Strings
####
def obj_type_string(hwloc_obj_type_t type1):
	return str(hwloc_obj_type_string(type1)[0:].decode('utf-8'))

#deprecated:
def obj_type_of_string(string):
	cdef hwloc_obj_type_t t
	string = _utfate(string)
	t = hwloc_obj_type_of_string(string)
	if <int>t == -1:
		raise ArgError('hwloc_obj_type_of_string')
	return int(t)

def obj_type_sscanf(string):
	"""Returns (hwloc_obj_type_t, int depth or None, hwloc_obj_cache_type_t or None)"""
	cdef hwloc_obj_type_t t
	cdef int depth
	cdef hwloc_obj_cache_type_t ct
	cdef size_t size
	string = _utfate(string)
	__checkneg1(hwloc_obj_type_sscanf(string, &t, &depth, &ct, sizeof(ct)))
	ict = int(ct)
	pydepth = int(depth)
	if ict == -1:
		ict = None
	if depth == -1:
		pydepth = None
	return int(t), pydepth, ict

def obj_type_asprintf(obj_ptr obj, int verbose):
	cdef char* string = NULL
	cdef size_t size = 0
	size = hwloc_obj_type_snprintf(string, size, obj.ptr(), verbose) + 1
	string = <char*>CMalloc(size+1)
	if string == NULL:
		raise OSError(CErrno, CStrerror(CErrno))
	size = hwloc_obj_type_snprintf(string, size, obj.ptr(), verbose)
	b = string[:int(size)].decode('utf8')
	CFree(string)
	return str(b)

def obj_attr_asprintf(obj_ptr obj, separator, int verbose):
	cdef char* string = NULL
	cdef size_t size = 0
	separator = _utfate(separator)
	size = hwloc_obj_attr_snprintf(string, size, obj.ptr(), separator, verbose) + 1
	string = <char*>CMalloc(size+1)
	if string == NULL:
		raise OSError(CErrno, CStrerror(CErrno))
	size = hwloc_obj_attr_snprintf(string, size, obj.ptr(), separator, verbose)
	b = string[:int(size)].decode('utf8')
	CFree(string)
	return str(b)

#deprecated
def obj_asprintf(__topology_handle topology, obj_ptr obj, indexprefix, int verbose):
	cdef char* string = NULL
	cdef size_t size = 0
	indexprefix = _utfate(indexprefix)
	size = hwloc_obj_snprintf(string, size, topology.ptr(), obj.ptr(),
							  indexprefix, verbose) + 1
	string = <char*>CMalloc(size+1)
	if string == NULL:
		raise OSError(CErrno, CStrerror(CErrno))
	size = hwloc_obj_snprintf(string, size, topology.ptr(), obj.ptr(),
							  indexprefix, verbose)
	b = string[:int(size)].decode('utf8')
	CFree(string)
	return str(b)

def obj_cpuset_asprintf(objs):
	cdef char* string = NULL
	cdef size_t size = 0
	cdef size_t nbobjs = len(objs)
	cdef hwloc_obj_t* p
	p = <hwloc_obj_t*>CMalloc(sizeof(hwloc_obj_t*) * nbobjs)
	if p == NULL:
		raise OSError(CErrno, CStrerror(CErrno))
	try:
		i = 0
		try:
			for j in objs:
				p[i] = (<obj_ptr>j).ptr()
				i += 1
		except:
			raise ArgError('obj_cpuset_asprintf')
		size = hwloc_obj_cpuset_snprintf(string, size, nbobjs, p) + 1
		string = <char*>CMalloc(size+1)
		if string == NULL:
			raise OSError(CErrno, CStrerror(CErrno))
		size = hwloc_obj_cpuset_snprintf(string, size, nbobjs, p)
		b = string[:int(size)].decode('utf8')
		CFree(string)
	finally:
		CFree(p)
	return str(b)

def obj_get_info_by_name(obj_ptr obj, name):
	name = _utfate(name)
	cdef const char* c = hwloc_obj_get_info_by_name(obj.ptr(), name)
	if c == NULL:
		return None
	return str(c.decode('utf8'))

def obj_add_info(obj_ptr obj, name, value):
	value = _utfate(value)
	name = _utfate(name)
	hwloc_obj_add_info(obj.ptr(), name, value)

####
# CPU binding
####
def set_cpubind(__topology_handle topology, __bitmap_ptr set1, int flags):
	__checkneg1(hwloc_set_cpubind(topology.ptr(), set1.ptr(), flags))

def get_cpubind(__topology_handle topology, int flags):
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_cpubind(topology.ptr(), b.ptr(), flags))
	return b

def set_proc_cpubind(__topology_handle topology, hwloc_pid_t pid, __bitmap_ptr set1, int flags):
	__checkneg1(hwloc_set_proc_cpubind(topology.ptr(), pid, set1.ptr(), flags))

def get_proc_cpubind(__topology_handle topology, hwloc_pid_t pid, int flags):
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_proc_cpubind(topology.ptr(), pid, b.ptr(), flags))
	return b

def set_thread_cpubind(__topology_handle topology, hwloc_thread_t thread,
					   __bitmap_ptr set1, int flags):
	__checkneg1(hwloc_set_thread_cpubind(topology.ptr(), thread, set1.ptr(),
										 flags))
def get_thread_cpubind(__topology_handle topology, hwloc_thread_t thread, int flags):
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_thread_cpubind(topology.ptr(), thread, b.ptr(),
										 flags))
	return b

def get_last_cpu_location(__topology_handle topology, int flags):
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_last_cpu_location(topology.ptr(), b.ptr(), flags))
	return b

def get_proc_last_cpu_location(__topology_handle topology, hwloc_pid_t pid, int flags):
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_proc_last_cpu_location(topology.ptr(), pid, b.ptr(),
											flags))
	return b

####
# Memory binding policy
####
def set_membind_nodeset(__topology_handle topology, __bitmap_ptr nodeset,
						hwloc_membind_policy_t policy, int flags):
	__checkneg1(hwloc_set_membind_nodeset(topology.ptr(), nodeset.ptr(), policy,
										  flags))

def set_membind(__topology_handle topology, __bitmap_ptr cpuset,
				hwloc_membind_policy_t policy, int flags):
	__checkneg1(hwloc_set_membind(topology.ptr(), cpuset.ptr(), policy, flags))

def get_membind_nodeset(__topology_handle topology, int flags):
	cdef hwloc_membind_policy_t p
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_membind_nodeset(topology.ptr(), b.ptr(), &p, flags))
	return b, int(p)

def get_membind(__topology_handle topology, int flags):
	cdef hwloc_membind_policy_t p
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_membind(topology.ptr(), b.ptr(), &p, flags))
	return b, int(p)

def set_proc_membind_nodeset(__topology_handle topology, hwloc_pid_t pid, __bitmap_ptr nodeset,
							 hwloc_membind_policy_t policy, int flags):
	__checkneg1(hwloc_set_proc_membind_nodeset(topology.ptr(), pid,
											   nodeset.ptr(), policy, flags))

def set_proc_membind(__topology_handle topology, hwloc_pid_t pid, __bitmap_ptr cpuset,
							 hwloc_membind_policy_t policy, int flags):
	__checkneg1(hwloc_set_proc_membind(topology.ptr(), pid,
									   cpuset.ptr(), policy, flags))

def get_proc_membind_nodeset(__topology_handle topology, hwloc_pid_t pid, int flags):
	cdef hwloc_membind_policy_t p
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_proc_membind_nodeset(topology.ptr(), pid, b.ptr(), &p,
										  flags))
	return b, int(p)

def get_proc_membind(__topology_handle topology, hwloc_pid_t pid, int flags):
	cdef hwloc_membind_policy_t p
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_proc_membind(topology.ptr(), pid, b.ptr(), &p, flags))
	return b, int(p)

def set_area_membind_nodeset(__topology_handle topology, unsigned long addr, size_t len1,
							 __bitmap_ptr nodeset, hwloc_membind_policy_t policy,
							 int flags):
	__checkneg1(hwloc_set_area_membind_nodeset(topology.ptr(), <void*>addr, len1,
											   nodeset.ptr(), policy, flags))

def set_area_membind(__topology_handle topology, unsigned long addr, size_t len1,
					 __bitmap_ptr set_, hwloc_membind_policy_t policy, int flags):
	__checkneg1(hwloc_set_area_membind(topology.ptr(), <void*>addr, len1,
									   set_.ptr(), policy, flags))

def get_area_membind_nodeset(__topology_handle topology, unsigned long addr, size_t len1,
							 int flags):
	cdef hwloc_membind_policy_t p
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_area_membind_nodeset(topology.ptr(), <void*>addr, len1,
											   b.ptr(), &p, flags))
	return b, int(p)

def get_area_membind(__topology_handle topology, unsigned long addr, size_t len1,
							 int flags):
	cdef hwloc_membind_policy_t p
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_area_membind(topology.ptr(), <void*>addr, len1,
									   b.ptr(), &p, flags))
	return b, int(p)

def get_area_memlocation(__topology_handle topology, unsigned long addr,
						 size_t len_, int flags):
	b = __bitmap_alloc()
	__checkneg1(hwloc_get_area_memlocation(topology.ptr(), <void*>addr, len_,
										   b.ptr(), flags))

def alloc(__topology_handle topology, size_t len1):
	return int(<unsigned long>__checknull(hwloc_alloc(topology.ptr(), len1)))

def alloc_membind_nodeset(__topology_handle topology, size_t len1, __bitmap_ptr nodeset,
						  hwloc_membind_policy_t policy, int flags):
	return int(<unsigned long>
			   __checknull(hwloc_alloc_membind_nodeset(topology.ptr(), len1,
													   nodeset.ptr(), policy,
													   flags)))

def alloc_membind(__topology_handle topology, size_t len1, __bitmap_ptr set_,
						  hwloc_membind_policy_t policy, int flags):
	return int(<unsigned long>
			   __checknull(hwloc_alloc_membind(topology.ptr(), len1,
											   set_.ptr(), policy, flags)))

# not sure there's a point to these two, but here they are:
def alloc_membind_policy_nodeset(__topology_handle topology, size_t len1,
								 __bitmap_ptr nodeset, hwloc_membind_policy_t policy,
								 int flags):
	return int(<unsigned long>
			   __checknull(hwloc_alloc_membind_policy_nodeset(topology.ptr(),
															  len1, nodeset.ptr(),
															  policy, flags)))

def alloc_membind_policy(__topology_handle topology, size_t len1, __bitmap_ptr set_,
						 hwloc_membind_policy_t policy, int flags):
	return int(<unsigned long>
			   __checknull(hwloc_alloc_membind_policy(topology.ptr(), len1,
													  set_.ptr(), policy, flags)))

def free(__topology_handle topology, unsigned long addr, size_t len1):
	__checkneg1(hwloc_free(topology.ptr(), <void*>addr, len1))

####
# Modifying a loaded Topology
####
def topology_insert_misc_object_by_cpuset(__topology_handle topology,
										  __bitmap_ptr cpuset, name):
	name = _utfate(name)
	return __omake(hwloc_topology_insert_misc_object_by_cpuset(topology.ptr(),
															   cpuset.ptr(),
															   name))

def topology_insert_misc_object_by_parent(__topology_handle topology, obj_ptr parent,
										  name):
	name = _utfate(name)
	return __omake(hwloc_topology_insert_misc_object_by_parent(topology.ptr(),
															   parent.ptr(),
															   name))

def topology_restrict(__topology_handle topology, __bitmap_ptr cpuset,
					  unsigned long flags):
	__checkneg1(hwloc_topology_restrict(topology.ptr(), cpuset.ptr(), flags))

def topology_dup(__topology_handle oldtopology):
	cdef topology_ptr newtopology = topology_ptr(init=False)
	__checkneg1(hwloc_topology_dup(<hwloc_topology_t*>&newtopology._pointer,
								   oldtopology.ptr()))
	return newtopology

####
# Building Custom Topologies
####
def custom_insert_topology(__topology_handle newtopology, obj_ptr newparent,
						   __topology_handle oldtopology, obj_ptr oldroot):
	__checkneg1(hwloc_custom_insert_topology(newtopology.ptr(), newparent.ptr(),
											 oldtopology.ptr(), __oget(oldroot)))

def custom_insert_group_object_by_parent(__topology_handle topology, obj_ptr parent,
										 int groupdepth):
	p = obj_ptr()
	p.set(__checknull(hwloc_custom_insert_group_object_by_parent(topology.ptr(),
																 parent.ptr(),
																 groupdepth)))
	return p

####
# Exporting Topologies to XML
####
def topology_export_xml(__topology_handle topology, xmlpath):
	xmlpath = _utfate(xmlpath)
	__checkneg1(hwloc_topology_export_xml(topology.ptr(), xmlpath))

def topology_export_xmlbuffer(__topology_handle topology):
	cdef char* xmlbuffer
	cdef int buflen
	__checkneg1(hwloc_topology_export_xmlbuffer(topology.ptr(), &xmlbuffer,
												&buflen))
	s = xmlbuffer[:buflen].decode('utf8')
	hwloc_free_xmlbuffer(topology.ptr(), xmlbuffer)
	return str(s)

def topology_set_userdata_export_callback(__topology_handle topology, cb):
	__userdata_export_callbacks[<unsigned long>topology.ptr()] = cb
	if cb is None:
		hwloc_topology_set_userdata_export_callback(topology.ptr(), NULL)
	else:
		hwloc_topology_set_userdata_export_callback(topology.ptr(),
													&__userdata_export_callback)


def export_obj_userdata(unsigned long reserved, __topology_handle topology, obj_ptr obj,
	name, buffer1):
	name = _utfate(name)
	buffer1 = _utfate(buffer1)
	__checkneg1(hwloc_export_obj_userdata(<void*>reserved, topology.ptr(),
										  obj.ptr(), name, <char*>buffer1, len(buffer1)))

def export_obj_userdata_base64(unsigned long reserved, __topology_handle topology,
						  obj_ptr obj, name, buffer1):
	name = _utfate(name)
	buffer1 = _utfate(buffer1)
	__checkneg1(hwloc_export_obj_userdata_base64(<void*>reserved, topology.ptr(),
										  obj.ptr(), name, <char*>buffer1, len(buffer1)))

def topology_set_userdata_import_callback(__topology_handle topology, cb):
	__userdata_import_callbacks[<unsigned long>topology.ptr()] = cb
	if cb is None:
		hwloc_topology_set_userdata_import_callback(topology.ptr(), NULL)
	else:
		hwloc_topology_set_userdata_import_callback(topology.ptr(),
													&__userdata_import_callback)

####
# Exporting Topologies to Synthetic
####
def topology_export_synthetic(__topology_handle topology, int flags):
	string = <char*>__checknull(CMalloc(1025))
	try:
		size = __checkneg1(hwloc_topology_export_synthetic(topology.ptr(),
														   string, 1024, flags))
		b = string[:int(size)].decode('utf8')
	finally:
		CFree(string)
	return str(b)


####
# Finding Objects Inside a CPU set
####
def get_first_largest_obj_inside_cpuset(__topology_handle topology, __bitmap_ptr set1):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_first_largest_obj_inside_cpuset(topology.ptr(),
																set1.ptr())))
	return p

def get_largest_objs_inside_cpuset(__topology_handle topology, __bitmap_ptr set1,
								   int max1):
	cdef hwloc_obj_t* objs
	objs = <hwloc_obj_t*>__checknull(CMalloc(sizeof(hwloc_obj_t)*max1))
	res = int(hwloc_get_largest_objs_inside_cpuset(topology.ptr(), set1.ptr(),
												   objs, max1))
	if res == -1:
		CFree(objs)
		raise ArgError('hwloc_get_largest_objs_inside_cpuset')
	l = []
	cdef size_t i
	for i in range(res):
		p = obj_ptr()
		p.set(objs[i])
		l.append(p)
	CFree(objs)
	return tuple(l)

def get_next_obj_inside_cpuset_by_depth(__topology_handle topology, __bitmap_ptr set1,
										int depth, obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_obj_inside_cpuset_by_depth(topology.ptr(),
																set1.ptr(),
																depth,
																__oget(prev))))
	return p

def get_next_obj_inside_cpuset_by_type(__topology_handle topology, __bitmap_ptr set1,
									   hwloc_obj_type_t type1, obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_obj_inside_cpuset_by_type(topology.ptr(),
															   set1.ptr(),
															   type1,
															   __oget(prev))))
	return p

def get_obj_inside_cpuset_by_depth(__topology_handle topology, __bitmap_ptr set1, int depth,
								   unsigned idx):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_obj_inside_cpuset_by_depth(topology.ptr(),
														   set1.ptr(), depth,
														   idx)))
	return p

def get_obj_inside_cpuset_by_type(__topology_handle topology, __bitmap_ptr set1,
								  hwloc_obj_type_t type1, unsigned idx):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_obj_inside_cpuset_by_type(topology.ptr(),
														  set1.ptr(), type1,
														  idx)))
	return p

def get_nbobjs_inside_cpuset_by_depth(__topology_handle topology, __bitmap_ptr set1, int depth):
	return int(hwloc_get_nbobjs_inside_cpuset_by_depth(topology.ptr(),
													   set1.ptr(), depth))

def get_nbobjs_inside_cpuset_by_type(__topology_handle topology, __bitmap_ptr set1,
									 hwloc_obj_type_t type1):
	return int(hwloc_get_nbobjs_inside_cpuset_by_type(topology.ptr(),
													  set1.ptr(), type1))

def get_obj_index_inside_cpuset(__topology_handle topology, __bitmap_ptr set1,
								obj_ptr obj):
	return int(hwloc_get_obj_index_inside_cpuset(topology.ptr(), set1.ptr(),
												 obj.ptr()))

####
# Finding a single Object covering at least a CPU set
####
def get_child_covering_cpuset(__topology_handle topology, __bitmap_ptr set1,
							  obj_ptr parent):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_child_covering_cpuset(topology.ptr(),
													  set1.ptr(),
													  parent.ptr())))
	return p

def get_obj_covering_cpuset(__topology_handle topology, __bitmap_ptr set1):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_obj_covering_cpuset(topology.ptr(),
													  set1.ptr())))
	return p

####
# Finding a set of similar Objects covering at least a CPU set
####
def get_next_obj_covering_cpuset_by_depth(__topology_handle topology, __bitmap_ptr set1,
										  int depth, obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_obj_covering_cpuset_by_depth(topology.ptr(),
																  set1.ptr(),
																  depth,
																  __oget(prev))))
	return p

def get_next_obj_covering_cpuset_by_type(__topology_handle topology, __bitmap_ptr set1,
										 hwloc_obj_type_t type1, obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_obj_covering_cpuset_by_type(topology.ptr(),
																 set1.ptr(),
																 type1,
																 __oget(prev))))
	return p

####
# Looking at Ancestor and Child Objects
####
def get_ancestor_obj_by_depth(__topology_handle topology, int depth, obj_ptr obj):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_ancestor_obj_by_depth(__tget(topology), depth,
													  obj.ptr())))
	return p

def get_ancestor_obj_by_type(__topology_handle topology, hwloc_obj_type_t type1, obj_ptr obj):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_ancestor_obj_by_type(__tget(topology), type1,
													 obj.ptr())))
	return p

def get_common_ancestor_obj(__topology_handle topology, obj_ptr obj1, obj_ptr obj2):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_common_ancestor_obj(__tget(topology), obj1.ptr(),
													obj2.ptr())))
	return p

def obj_is_in_subtree(__topology_handle topology, obj_ptr obj, obj_ptr subtree_root):
	return int(hwloc_obj_is_in_subtree(__tget(topology), obj.ptr(),
									   subtree_root.ptr()))

def get_next_child(__topology_handle topology, obj_ptr parent, obj_ptr prev):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_next_child(__tget(topology), parent.ptr(),
										   __oget(prev))))
	return p

####
# Looking at Cache Objects
####
def get_cache_type_depth(__topology_handle topology, unsigned cachelevel,
						 hwloc_obj_cache_type_t cachetype):
	return int(hwloc_get_cache_type_depth(topology.ptr(), cachelevel, cachetype))

def get_cache_covering_cpuset(__topology_handle topology, __bitmap_ptr set1):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_cache_covering_cpuset(topology.ptr(),
													  set1.ptr())))
	return p

def get_shared_cache_covering_obj(__topology_handle topology, obj_ptr obj):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_shared_cache_covering_obj(__tget(topology),
														  obj.ptr())))
	return p

####
# Finding objects, miscellaneous helpers
####
def get_pu_obj_by_os_index(__topology_handle topology, unsigned os_index):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_pu_obj_by_os_index(topology.ptr(), os_index)))
	return p

def get_numanode_obj_by_os_index(__topology_handle topology, unsigned os_index):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_numanode_obj_by_os_index(topology.ptr(),
														 os_index)))
	return p

def get_closest_objs(__topology_handle topology, obj_ptr src, unsigned max1):
	cdef hwloc_obj_t* objs
	objs = <hwloc_obj_t*>__checknull(CMalloc(sizeof(hwloc_obj_t)*max1))
	res = int(hwloc_get_closest_objs(topology.ptr(), src.ptr(), objs, max1))
	l = []
	cdef size_t i
	for i in range(res):
		p = obj_ptr()
		p.set(objs[i])
		l.append(p)
	CFree(objs)
	return tuple(l)

def get_obj_below_by_type(__topology_handle topology, hwloc_obj_type_t type1,
						  unsigned idx1, hwloc_obj_type_t type2, unsigned idx2):
	p = obj_ptr()
	p.set(__checknone(hwloc_get_obj_below_by_type(topology.ptr(), type1, idx1,
												  type2, idx2)))
	return p

def get_obj_below_array_by_type(__topology_handle topology, typev, idxv):
	if len(typev) != len(idxv):
		raise ArgError('get_obj_below_array_by_type')
	nr = len(typev)
	cdef hwloc_obj_type_t* typep
	typep = <hwloc_obj_type_t*>__checknull(CMalloc(sizeof(hwloc_obj_type_t)*nr))
	cdef unsigned* idxp
	idxp = <unsigned*>__checknull(CMalloc(sizeof(unsigned)*nr))
	cdef size_t i
	for i in range(nr):
		typep[i] = typev[i]
		idxp[i] = idxv[i]
	try:
		p = obj_ptr()
		p.set(__checknone(hwloc_get_obj_below_array_by_type(topology.ptr(), nr,
															typep, idxp)))
	finally:
		CFree(typep)
		CFree(idxp)
	return p

####
# Distributing items over a topology
####
def distrib(__topology_handle topology, roots, unsigned n, unsigned until, unsigned flags):
	cdef hwloc_cpuset_t* cpuset
	set1 = <hwloc_cpuset_t*>__checknull(CMalloc(sizeof(hwloc_bitmap_t)*n))
	cdef hwloc_obj_t* rootp
	n_roots = len(roots)
	try:
		rootp = <hwloc_obj_t*>__checknull(CMalloc(sizeof(hwloc_obj_t)*n_roots))
	except OSError as e:
		CFree(set1)
		raise e
	cdef size_t i
	for i in range(n_roots):
		rootp[i] = (<obj_ptr>roots[i]).ptr()
	hwloc_distrib(topology.ptr(), rootp, n_roots, set1, n, until, flags)
	CFree(rootp)
	l = []
	try:
		for i in range(n):
			l.append(__bnew(set1[i]))
	finally:
		CFree(set1)
	return tuple(l)

#deprecated
def distribute(__topology_handle topology, obj_ptr root, unsigned n, unsigned until):
	cdef hwloc_cpuset_t* set1
	set1 = <hwloc_cpuset_t*>__checknull(CMalloc(sizeof(hwloc_bitmap_t)*n))
	hwloc_distribute(topology.ptr(), root.ptr(), set1, n, until)
	l = []
	cdef size_t i
	try:
		for i in range(n):
			p = volatile_bitmap_ptr()
			p.set(__checknone(set1[i]))
			l.append(p)
	finally:
		CFree(set1)
	return tuple(l)

#deprecated
distributev = distrib


####
# CPU and node sets of entire topologies
####
def topology_get_complete_cpuset(__topology_handle topology):
	return __bmake(hwloc_topology_get_complete_cpuset(topology.ptr()))

def topology_get_topology_cpuset(__topology_handle topology):
	return __bmake(hwloc_topology_get_topology_cpuset(topology.ptr()))

def topology_get_online_cpuset(__topology_handle topology):
	return __bmake(hwloc_topology_get_online_cpuset(topology.ptr()))

def topology_get_allowed_cpuset(__topology_handle topology):
	return __bmake(hwloc_topology_get_allowed_cpuset(topology.ptr()))

def topology_get_complete_nodeset(__topology_handle topology):
	return __bmake(hwloc_topology_get_complete_nodeset(topology.ptr()))

def topology_get_topology_nodeset(__topology_handle topology):
	return __bmake(hwloc_topology_get_topology_nodeset(topology.ptr()))

def topology_get_allowed_nodeset(__topology_handle topology):
	return __bmake(hwloc_topology_get_allowed_nodeset(topology.ptr()))


####
# Converting between CPU sets and node sets
####
def cpuset_to_nodeset(__topology_handle topology, __bitmap_ptr cpuset):
	"""Convert a CPU set into a NUMA node set and handle non-NUMA cases"""
	nodeset = __bitmap_alloc()
	hwloc_cpuset_to_nodeset(topology.ptr(), cpuset.ptr(), nodeset.ptr())
	return nodeset

def cpuset_to_nodeset_strict(__topology_handle topology, __bitmap_ptr cpuset):
	"""Convert a CPU set into a NUMA node set without handling non-NUMA cases"""
	nodeset = __bitmap_alloc()
	hwloc_cpuset_to_nodeset_strict(topology.ptr(), cpuset.ptr(),
								   nodeset.ptr())
	return nodeset

def cpuset_from_nodeset(__topology_handle topology, __bitmap_ptr nodeset):
	"""Convert a NUMA node set into a CPU set and handle non-NUMA cases"""
	cpuset = __bitmap_alloc()
	hwloc_cpuset_from_nodeset(topology.ptr(), cpuset.ptr(),
								   nodeset.ptr())
	return cpuset

def cpuset_from_nodeset_strict(__topology_handle topology, __bitmap_ptr nodeset):
	"""Convert a NUMA node set into a CPU set and handle non-NUMA cases"""
	cpuset = __bitmap_alloc()
	hwloc_cpuset_from_nodeset_strict(topology.ptr(), cpuset.ptr(),
								   nodeset.ptr())
	return cpuset


####
# Manipulating Distances
####
def get_whole_distance_matrix_by_depth(__topology_handle topology, int depth):
	"""Get the distances between all objects at the given depth"""
	p = distances_ptr()
	p.set(__checknone(hwloc_get_whole_distance_matrix_by_depth(topology.ptr(),
															   depth)))
	return p

def get_whole_distance_matrix_by_type(__topology_handle topology, hwloc_obj_type_t type1):
	"""Get the distances between all objects of a given type"""
	p = distances_ptr()
	p.set(__checknone(hwloc_get_whole_distance_matrix_by_type(topology.ptr(),
															  type1)))
	return p

def get_distance_matrix_covering_obj_by_depth(__topology_handle topology, obj_ptr obj,
											  int depth):
	"""Get distances for the given depth and covering some objects.
	Returns (distances, logical index of 1st object)"""
	cdef unsigned first
	p = distances_ptr()
	p.set(__checknone(hwloc_get_distance_matrix_covering_obj_by_depth(topology.ptr(),
																	  obj.ptr(),
																	  depth,
																	  &first)))
	return p

def get_latency(__topology_handle topology, obj_ptr obj1, obj_ptr obj2):
	"""Get the latency in both directions between two objects
	Returns (latency, reverse latency)"""
	cdef float latency = 0.0, reverse_latency = 0.0
	__checkneg1(hwloc_get_latency(topology.ptr(), obj1.ptr(), obj2.ptr(),
								  &latency, &reverse_latency))
	return float(latency), float(reverse_latency)


####
# Finding I/O objects
####
def get_non_io_ancestor_obj(__topology_handle topology, obj_ptr ioobj):
	"""Get the first non-I/O ancestor object"""
	return __omake(hwloc_get_non_io_ancestor_obj(__tget(topology), ioobj.ptr()))

def get_next_pcidev(__topology_handle topology, obj_ptr prev):
	"""Get the next PCI device in the system"""
	return __omake(hwloc_get_next_pcidev(topology.ptr(), __oget(prev)))

def get_pcidev_by_busid(__topology_handle topology, unsigned domain, unsigned bus, unsigned dev,
						unsigned func):
	"""Find the PCI device object matching the PCI bus id
	given domain, bus device and function PCI bus id"""
	return __omake(hwloc_get_pcidev_by_busid(topology.ptr(), domain, bus, dev,
											 func))

def get_pcidev_by_busidstring(__topology_handle topology, busid):
	"""Find the PCI device object matching the PCI bus id
	given as a string xxxx:yy:zz.t or yy:zz.t"""
	busid = _utfate(busid)
	return __omake(hwloc_get_pcidev_by_busidstring(topology.ptr(), busid))

def get_next_osdev(__topology_handle topology, obj_ptr prev):
	"""Get the next OS device in the system"""
	return __omake(hwloc_get_next_osdev(topology.ptr(), __oget(prev)))

def get_next_bridge(__topology_handle topology, obj_ptr prev):
	return __omake(hwloc_get_next_bridge(topology.ptr(), __oget(prev)))

def bridge_covers_pcibus(obj_ptr bridge, unsigned domain, unsigned bus):
	return int(hwloc_bridge_covers_pcibus(bridge.ptr(), domain, bus))

def get_hostbridge_by_pcibus(__topology_handle topology, unsigned domain, unsigned bus):
	return __omake(hwloc_get_hostbridge_by_pcibus(topology.ptr(), domain, bus))


####
# Topology differences
####
cdef class __ptr_backref(__ptr):
	cdef __ptr _backref

	def __init__(self, ref=None):
		self._backref = ref

	# hold a reference to keep __dealloc__ from being called if the pointer
	# to the first diff goes away.
	def set_backref(self, instance):
		self._backref = instance

cdef class diff_obj_attr_generic_ptr(__ptr_backref):
	cdef hwloc_topology_diff_obj_attr_generic_s* ptr(self):
		return <hwloc_topology_diff_obj_attr_generic_s*>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)

cdef class diff_obj_attr_uint64_ptr(__ptr_backref):
	cdef hwloc_topology_diff_obj_attr_uint64_s* ptr(self):
		return <hwloc_topology_diff_obj_attr_uint64_s*>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)

	property index:
		def __get__(self):
			return int(self.ptr().index)

	property oldvalue:
		def __get__(self):
			return int(self.ptr().oldvalue)

	property newvalue:
		def __get__(self):
			return int(self.ptr().newvalue)

cdef class diff_obj_attr_string_ptr(__ptr_backref):
	cdef hwloc_topology_diff_obj_attr_string_s* ptr(self):
		return <hwloc_topology_diff_obj_attr_string_s*>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)

	property name:
		def __get__(self):
			return str(<bytes>self.ptr().name.decode('utf8'))

	property oldvalue:
		def __get__(self):
			return str(<bytes>self.ptr().oldvalue.decode('utf8'))

	property newvalue:
		def __get__(self):
			return str(<bytes>self.ptr().newvalue.decode('utf8'))

cdef class diff_obj_attr_u_ptr(__ptr_backref):

	property generic:
		def __get__(self):
			p = diff_obj_attr_generic_ptr(self)
			p.set(self.get())
			return p

	property uint64:
		def __get__(self):
			p = diff_obj_attr_uint64_ptr(self)
			p.set(self.get())
			return p

	property string:
		def __get__(self):
			p = diff_obj_attr_string_ptr(self)
			p.set(self.get())
			return p

cdef class diff_generic_ptr(__ptr_backref):
	cdef hwloc_topology_diff_generic_s* ptr(self):
		return <hwloc_topology_diff_generic_s*>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)

	property next:
		def __get__(self):
			if self.ptr().next == NULL:
				return None
			p = __topology_diff_ptr(self)
			p.set(self.ptr().next)
			return p

cdef class diff_obj_attr_s_ptr(__ptr_backref):
	cdef hwloc_topology_diff_obj_attr_s* ptr(self):
		return <hwloc_topology_diff_obj_attr_s*>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)

	property next:
		def __get__(self):
			if self.ptr().next == NULL:
				return None
			p = __topology_diff_ptr(self)
			p.set(self.ptr().next)
			return p

	property obj_depth:
		def __get__(self):
			return int(self.ptr().obj_depth)

	property obj_index:
		def __get__(self):
			return int(self.ptr().obj_index)

	property diff:
		def __get__(self):
			p = diff_obj_attr_u_ptr(self)
			p.set(&self.ptr().diff)
			return p

cdef class diff_too_complex_ptr(__ptr_backref):
	cdef hwloc_topology_diff_too_complex_s* ptr(self):
		return <hwloc_topology_diff_too_complex_s*>self.get()

	property type:
		def __get__(self):
			return int(self.ptr().type)

	property next:
		def __get__(self):
			if self.ptr().next == NULL:
				return None
			p = __topology_diff_ptr(self)
			p.set(self.ptr().next)
			return p

	property obj_depth:
		def __get__(self):
			return int(self.ptr().obj_depth)

	property obj_index:
		def __get__(self):
			return int(self.ptr().obj_index)

cdef class __topology_diff_ptr(__ptr_backref):
	cdef hwloc_topology_diff_t ptr(self):
		return <hwloc_topology_diff_t>self.get()

	property generic:
		def __get__(self):
			p = diff_generic_ptr(self)
			p.set(self.get())
			return p

	property obj_attr:
		def __get__(self):
			p = diff_obj_attr_s_ptr(self)
			p.set(self.get())
			return p

	property too_complex:
		def __get__(self):
			p = diff_too_complex_ptr(self)
			p.set(self.get())
			return p

cdef class topology_diff_ptr(__topology_diff_ptr):
	def __dealloc__(self):
		if self._pointer != NULL:
			t = self._backref.get()
			hwloc_topology_diff_destroy(<hwloc_topology_t>t,
										<hwloc_topology_diff_t>self.get())

def topology_diff_build(__topology_handle topology,
						__topology_handle newtopology, unsigned long flags = 0):
	"""returns topology_diff_ptr, (boolean) is too complex"""
	cdef hwloc_topology_diff_t diffp
	cdef int ret
	ret = hwloc_topology_diff_build(topology.ptr(), newtopology.ptr(), flags,
									&diffp)
	__checkneg1(ret)
	if diffp == NULL:
		return None, False
	diff = topology_diff_ptr(topology)
	diff.set(diffp)
	return diff, ret == 1

def topology_diff_apply(__topology_handle topology, topology_diff_ptr diff,
						unsigned long flags):
	return int(hwloc_topology_diff_apply(topology.ptr(), diff.ptr(), flags))

def topology_diff_load_xml(__topology_handle topology, const char *xmlpath):
	"""returns topology_diff_ptr, refname"""
	cdef hwloc_topology_diff_t diffp
	cdef char *refname
	x = _utfate(xmlpath)
	__checkneg1(hwloc_topology_diff_load_xml(topology.ptr(), x, &diffp,
											 &refname))
	try:
		r = refname.decode('utf8')
	finally:
		CFree(refname)
	diff = topology_diff_ptr(topology)
	diff.set(diffp)
	return diff, str(r)

def topology_diff_export_xml(__topology_handle topology, topology_diff_ptr diff,
							 const char* refname, const char* xmlpath):
	r = None
	if refname is not None:
		r = _utfate(refname)
	x = _utfate(xmlpath)
	__checkneg1(hwloc_topology_diff_export_xml(topology.ptr(), diff.ptr(),
											   r, x))

def topology_diff_load_xmlbuffer(__topology_handle topology, xmlbuffer):
	"""returns topology_diff_ptr, refname"""
	cdef hwloc_topology_diff_t diffp
	cdef char *refname
	xmlbuffer = _utfate(xmlbuffer)
	__checkneg1(hwloc_topology_diff_load_xmlbuffer(topology.ptr(), xmlbuffer,
												   len(xmlbuffer), &diffp,
												   &refname))
	if refname == NULL:
		r = None
	else:
		r = refname.decode('utf8')
		CFree(refname)
		r = str(r)
	diff = topology_diff_ptr(topology)
	diff.set(diffp)
	return diff, r

def topology_diff_export_xmlbuffer(__topology_handle topology,
								   topology_diff_ptr diff, refname):
	cdef char* xmlbuffer
	cdef int buflen
	cdef char* r = NULL
	if refname is not None:
		refname = _utfate(refname)
		r = refname
	__checkneg1(hwloc_topology_diff_export_xmlbuffer(topology.ptr(), diff.ptr(),
													 r, &xmlbuffer, &buflen))
	try:
		x = xmlbuffer[:buflen].decode('utf8')
	finally:
		hwloc_free_xmlbuffer(topology.ptr(), xmlbuffer)
	return str(x)


####
# Linux-only helpers
####
cdef linux_parse_cpumap_file(FILE* fp):
	set1 = __bitmap_alloc()
	hwloc_linux_parse_cpumap_file(fp, set1.ptr())
	return set1

def linux_parse_cpumap(path):
	"""file path string, not a FILE pointer"""
	cdef FILE* fp = NULL
	path = _utfate(path)
	b = None
	try:
		fp = <FILE*>__checknull(CFopen(path, 'r'))
		b = linux_parse_cpumap_file(fp)
	finally:
		if fp != NULL:
			CFclose(fp)
	return b

def linux_set_tid_cpubind(__topology_handle topology, pid_t tid, __bitmap_ptr set1):
	__checkneg1(hwloc_linux_set_tid_cpubind(topology.ptr(), tid, set1.ptr()))

def linux_get_tid_cpubind(__topology_handle topology, pid_t tid):
	set1 = __bitmap_alloc()
	__checkneg1(hwloc_linux_get_tid_cpubind(topology.ptr(), tid, set1.ptr()))
	return set1

def linux_get_tid_last_cpu_location(__topology_handle topology, pid_t tid):
	set_ = __bitmap_alloc()
	__checkneg1(hwloc_linux_get_tid_last_cpu_location(topology.ptr(), tid,
													  set_.ptr()))
	return set_

####
# OpenGL display specific functions
####
def gl_get_display_osdev_by_port_device(__topology_handle topology, unsigned port,
										unsigned device):
	"""Get the hwloc OS device object corresponding to the
	OpenGL display given by port and device index"""
	return __omake(__checknull(hwloc_gl_get_display_osdev_by_port_device(topology.ptr(),
																		 port,
																		 device)))

def gl_get_display_osdev_by_name(__topology_handle topology, name):
	"""Get the hwloc OS device object corresponding to the
	OpenGL display given by name"""
	name = _utfate(name)
	return __omake(__checknull(hwloc_gl_get_display_osdev_by_name(topology.ptr(),
																   name)))

def gl_get_display_by_osdev(__topology_handle topology, obj_ptr osdev):
	"""Get the OpenGL display port and device corresponding
	to the given hwloc OS object.
	Returns (port, device)"""
	cdef unsigned port, device
	if hwloc_gl_get_display_by_osdev(__tget(topology), osdev.ptr(), &port, &device) == -1:
		raise NULLError
	return int(port), int(device)


####
# CUDA Driver API Specific Functions
####
#def cuda_get_device_pci_ids(__topology_handle topology, CUdevice cudevice):
#	"""Return the domain, bus and device IDs of the CUDA device"""
#	cdef int domain, bus, dev
#	__checkneg1(hwloc_cuda_get_device_pci_ids(topology.ptr(), cudevice,
#										#	  &domain, &bus, &dev))
#	return int(domain), int(bus), int(dev)
#
#def cuda_get_device_cpuset(__topology_handle topology, CUdevice cudevice):
#	"""Get the CPU set of logical processors that are physically
#	close to the CU device"""
#	b = __bitmap_alloc()
#	__checkneg1(hwloc_cuda_get_device_cpuset(topology.ptr(), cudevice,
#										#	 b.ptr()))
#	return b
#
#def cuda_get_device_pcidev(__topology_handle topology, CUdevice cudevice):
#	"""Get the hwloc PCI device object corresponding to the CUDA device"""
#	return __omake(hwloc_cuda_get_device_pcidev(topology.ptr(), cudevice))
#
#def cuda_get_device_osdev(__topology_handle topology, CUdevice cudevice):
#	"""Get the hwloc OS device object corresponding to the CUDA device"""
#	return __omake(hwloc_cuda_get_device_osdev(topology.ptr(), cudevice))
#

IF WITH_x86_64:
	####
	# Helpers for manipulating Linux libnuma unsigned long masks
	####
	import libnuma

	def cpuset_to_linux_libnuma_ulongs(__topology_handle topology, __bitmap_ptr cpuset):
		"""Convert hwloc CPU set into a tuple of unsigned long
		Returns: tuple of ints, maxnode"""
		cdef unsigned long* mask
		cdef unsigned long maxnode
		maxnode = libnuma.numa_max_node()
		size = int((maxnode+8*sizeof(unsigned long)-1)/8/sizeof(unsigned long))
		mask = <unsigned long*>__checknull(CMalloc(size*sizeof(unsigned long)))
		cdef size_t i
		try:
			hwloc_cpuset_to_linux_libnuma_ulongs(topology.ptr(), cpuset.ptr(), mask,
												&maxnode)
			size = int((maxnode+8*sizeof(unsigned long)-1)/8/sizeof(unsigned long))
			l = []
			for i in range(size):
				l.append(int(mask[i]))
		finally:
			CFree(mask)
		return tuple(l), maxnode

	def nodeset_to_linux_libnuma_ulongs(__topology_handle topology, __bitmap_ptr nodeset):
		"""Convert hwloc NUMA node set into the array of unsigned long
		Returns: tuple of ints, maxnode"""
		cdef unsigned long* mask
		cdef unsigned long maxnode
		maxnode = libnuma.numa_max_node()
		size = int((maxnode+8*sizeof(unsigned long)-1)/8/sizeof(unsigned long))
		mask = <unsigned long*>__checknull(CMalloc(size*sizeof(unsigned long)))
		cdef size_t i
		try:
			hwloc_nodeset_to_linux_libnuma_ulongs(topology.ptr(), nodeset.ptr(), mask,
												&maxnode)
			size = int((maxnode+8*sizeof(unsigned long)-1)/8/sizeof(unsigned long))
			l = []
			for i in range(size):
				l.append(int(mask[i]))
		finally:
			CFree(mask)
		return tuple(l), maxnode

	def cpuset_from_linux_libnuma_ulongs(__topology_handle topology, mask,
											maxnode=None):
		"""Convert a list of unsigned long into hwloc CPU set"""
		cdef unsigned long* cmask
		if maxnode is None:
			maxnode = libnuma.numa_max_node()
		b = __bitmap_alloc()
		cmask = <unsigned long*>__checknull(CMalloc(len(mask)*sizeof(unsigned long)))
		cdef size_t i
		try:
			for i in range(len(mask)):
				cmask[i] = mask[i]
			hwloc_cpuset_from_linux_libnuma_ulongs(topology.ptr(), b.ptr(), cmask,
													maxnode)
		finally:
			CFree(cmask)
		return b

	def nodeset_from_linux_libnuma_ulongs(__topology_handle topology, mask,
											maxnode=None):
		"""Convert a list of unsigned long into hwloc NUMA node set"""
		cdef unsigned long* cmask
		if maxnode is None:
			maxnode = libnuma.numa_max_node()
		b = __bitmap_alloc()
		cmask = <unsigned long*>__checknull(CMalloc(len(mask)*sizeof(unsigned long)))
		cdef size_t i
		try:
			for i in range(len(mask)):
				cmask[i] = mask[i]
			hwloc_nodeset_from_linux_libnuma_ulongs(topology.ptr(), b.ptr(), cmask,
													maxnode)
		finally:
			CFree(cmask)
		return b

	def cpuset_to_linux_libnuma_bitmask(__topology_handle topology,
										__bitmap_ptr cpuset):
		"""Convert hwloc CPU set into a python-libnuma Bitmask"""
		cdef bitmask* b
		b = <bitmask*>__checknull(hwloc_cpuset_to_linux_libnuma_bitmask(topology.ptr(),
																		cpuset.ptr()))
		n = libnuma.Bitmask()
		n.SetPtr(<unsigned long>b)
		return n

	def nodeset_to_linux_libnuma_bitmask(__topology_handle topology,
										__bitmap_ptr nodeset):
		"""Convert hwloc NUMA node set into a python-libnuma Bitmask"""
		cdef bitmask* b
		b = <bitmask*>__checknull(hwloc_nodeset_to_linux_libnuma_bitmask(topology.ptr(),
																		nodeset.ptr()))
		n = libnuma.Bitmask()
		n.SetPtr(<unsigned long>b)
		return n


	cdef const bitmask* __bmget(bm):
		cdef unsigned long p
		p = bm.Ptr()
		return <const bitmask*>p

	def cpuset_from_linux_libnuma_bitmask(__topology_handle topology, bitmask):
		"""Convert python-libnuma Bitmask into hwloc CPU set"""
		b = __bitmap_alloc()
		hwloc_cpuset_from_linux_libnuma_bitmask(topology.ptr(), b.ptr(),
												__bmget(bitmask))
		return b

	def nodeset_from_linux_libnuma_bitmask(__topology_handle topology, bitmask):
		"""Convert python-libnuma Bitmask into hwloc NUMA node set set"""
		b = __bitmap_alloc()
		hwloc_nodeset_from_linux_libnuma_bitmask(topology.ptr(), b.ptr(),
												__bmget(bitmask))
		return b
#ENDIF

####
# Intel Xeon Phi (MIC) Specific Functions
####
def intel_mic_get_device_cpuset(__topology_handle topology, int idx):
	"""Get the CPU set of logical processors that are physically close to MIC device whose index is idx"""
	b = __bitmap_alloc()
	__checkneg1(hwloc_intel_mic_get_device_cpuset(__tget(topology), idx, b.ptr()))
	return b

def intel_mic_get_device_osdev_by_index(__topology_handle topology, unsigned idx):
	"""Get the hwloc OS device object corresponding to the MIC device for the given index"""
	p = obj_ptr()
	p.set(__checknone(hwloc_intel_mic_get_device_osdev_by_index(topology.ptr(),
																idx)))
	return p


####
# NVIDIA Management Library Specific Functions
####
#def nvml_get_device_osdev_by_index(__topology_handle topology, unsigned idx):
#	"""Get the hwloc OS device object corresponding to the NVML device whose index is idx"""
#	p = obj_ptr()
#	p.set(__checknone(hwloc_nvml_get_device_osdev_by_index(topology.ptr(), idx)))
#	return p
