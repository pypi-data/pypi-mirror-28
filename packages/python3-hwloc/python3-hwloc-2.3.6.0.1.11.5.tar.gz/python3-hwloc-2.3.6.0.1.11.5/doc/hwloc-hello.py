#!/usr/bin/env python3
# -*- python -*-

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
# This is a re-implementation in python of hwloc-hello.c from the
# hwloc package.

import hwloc

def print_children(t, obj, depth):
    text = t.obj_asprintf(obj, '#', 0)
    print(' '*depth*2 + text)
    array = obj.children
    for a in array:
        print_children(t, a, depth+1)

topo = hwloc.Topology()

topo.load()

topodepth = topo.depth

for depth in range(topodepth):
    print('*** Objects at level %d' % (depth))
    for i in range(topo.get_nbobjs_by_depth(depth)):
        text = topo.obj_asprintf(topo.get_obj_by_depth(depth, i), '#', 0)
        print('Index %u: %s' % (i,  text))

o = topo.root_obj

print('*** Printing overall tree')
print_children(topo, o, 0)

depth = topo.get_type_depth(hwloc.OBJ_SOCKET)
if depth == hwloc.TYPE_DEPTH_UNKNOWN:
    print('*** The number of sockets is unknown')
else:
    print('*** %u socket(s)' % (topo.get_nbobjs_by_depth(depth)))

levels = 0
size = 0

obj = topo.get_obj_by_type(hwloc.OBJ_PU, 0)

while obj is not None:
    if obj.type == hwloc.OBJ_CACHE:
        levels += 1
        size += obj.attr.cache.size
    obj = obj.parent
print('*** Logical processor 0 has %d caches totaling %luKB' % (levels, size/1024))

depth = topo.get_type_or_below_depth(hwloc.OBJ_CORE)

obj = topo.get_obj_by_depth(depth, topo.get_nbobjs_by_depth(depth) - 1)

cpuset = obj.cpuset.dup()
cpuset.singlify()

try:
    topo.set_cpubind(cpuset, 0)
except:
    print("Couldn't bind to cpuset", cpuset.asprintf())

# alloc_membind doesn't make a lot of sense in python, since you really
# can't tell the python interpreter to use the space.
n = topo.get_nbobjs_by_type(hwloc.OBJ_NODE)
if n:
    size = 1024*1024
    obj = topo.get_obj_by_type(hwloc.OBJ_NODE, n - 1)
    m = topo.alloc_membind_nodeset(size, obj.nodeset, hwloc.MEMBIND_DEFAULT, 0) #TODO: should this work in python?
    del m
# I can't think of a way to use hwloc_set_area_membind* in python
    import ctypes
    s = ctypes.create_string_buffer(size)
    try:
        topo.set_area_membind_nodeset(ctypes.addressof(s), size, obj.nodeset, hwloc.MEMBIND_DEFAULT, 0)
    except OSError as err:
        print(str(err))
    del s
