# Application Developer Guide For `python-hwloc`
Copyright 2016-2017 Guy Streeter

*This copyrighted material is made available to anyone wishing to use, modify, copy, or redistribute it subject to the terms and conditions of the `GNU General Public License v.2`.*

*This material is distributed in the hope that it will be useful, but *WITHOUT ANY WARRANTY*; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.*

# Version information
* August 22 2017: This is the initial release of the document, corresponding to the package version 2.3-1.11.5

## Introduction
`python-hwloc` is a set of Python bindings for `hwloc`, the Portable Hardware Locality software package. The `python-hwloc` package allows access to the `hwloc` library from Python applications. Information on `hwloc` is available at <nobr><https://www.open-mpi.org/projects/hwloc></nobr>. The source code for `python-hwloc` is maintained at <nobr><https://gitlab.com/guystreeter/python-hwloc></nober>.

This document describes the implemented interface between Python and the `hwloc` library. The first section discusses obtaining and installing the `python-hwloc` package. The next sections describe the Python classes representing the C structures used in `hwloc`, with documentation of the methods and properties of each class. Some examples are inter-mixed with the documentation. The source code contains a `tests` folder providing further usage examples.

**Please Note** that this package is written for Linux, and has only been tested on recent Fedora&reg; and Red Hat&reg; systems. It should work on any recent Linux platform for which `hwloc` has been built.

## Installation
RPM package repositories for Fedora and for EPEL for Centos&reg; 7 are available at <nobr><https://copr.fedorainfracloud.org/coprs/streeter/python-hwloc></nobr>. For other linux platforms, the source code can be down-loaded from <nobr><https://gitlab.com/guystreeter/python-hwloc></nobr> and the `setup.py` file can be used to build and install it. Building `python-hwloc` requires Cython, and the development files for the `hwloc`, `numactl` (or `libnuma`), and `libibverbs` packages.

`python-hwloc` also requires `python-libnuma`, available from the same RPM repository. The source for `python-libnuma` is available at <nobr><https://gitlab.com/guystreeter/python-libnuma></nobr>.

This document can be recreated in the source tree using the command `make doc`. This requires the `pandoc` and `latex` applications.

## Differences from the C library
Wherever the C library uses structures, this package implements classes that allow access to the structure members as properties. If a structure member is a structure or structure pointer, the associated object property is an object. The object instances hold pointers to the `hwloc` library structures. Except where they are explicitly created, (bitmap allocation for instance), these library structures remain in place until the topology is destroyed. *A reference to the topology object should be held as long as any constituent object instance is needed.*

Generally, library functions that reference a structure are implemented as methods in the class that represents that structure. Some of the classes support the use of various Python operators, such as conversion to string or comparison.

The Python code handles reference counting, and the freeing of allocated structures when required. *Assignment to a new variable name does not copy the library structures, it just make a new reference to the same object instance.*

All of the library functions with names ending in `snprintf` have been changed to an `asprintf` implementation, and the caller is not responsible for providing a string buffer for the result. The returned value is a native Python string.

## Classes
The major classes used are `Topology`, `Obj`, and `Bitmap`. These correspond to the `hwloc_topology`, `hwloc_obj`, and `hwloc_bitmap` structures in the `hwloc` C code. They may for example be used as follows:

```python
#!/usr/bin/python3

import hwloc

topo = hwloc.Topology()
topo.load()

robj = topo.root_obj

bmap = robj.cpuset

print('root object cpuset is', str(bmap))
```
*Note* that unless otherwise specified, properties are read-only

### `ArgError`
`ArgError` is derived from the base Exception class. It is raised by class methods when one of the calling arguments is invalid. The exception object can be coerced to a string for error messages. For example
```python
#!/usr/bin/python3

from hwloc import Bitmap, ArgError

bmap = Bitmap()
try:
    bmap.sscanf('qwerty')
except ArgError as err:
    print(str(err))
```

### `Bitmap`
The `Bitmap` class represents the `hwloc_bitmap` structure, which is opaque to the application. The class has methods which can operate on the object instance, as well as object properties. It also has some class methods.

*Important Note About `Bitmap` Object Lifetimes*
`Bitmap` instances remember automatically if they were created by explicit allocation (or returned as a result of a function call), or if they are references to bitmaps in other objects. An allocated bitmap will be freed when the reference count of the instance goes to zero.  
Bitmaps that are references to other object properties are freed when that object instance goes away. A variable that is a reference to a bitmap property of another object will behave unpredictably when the underlying `hwloc` library structure is freed

Creating an instance of a `Bitmap` using the constructor (which must not have any parameters) is equivalent to calling the `alloc` class method without a parameter. These two statements are equivalent:
```python
bmap = Bitmap()

bmap = Bitmap.alloc()
```

#### Class methods
The class methods are:
* `alloc(values=None)`

> `alloc` can be called with a parameter. If the parameter is an `int`, that bit is set in the resulting `Bitmap`. If the parameter is a `str`, the resulting `Bitmap` is set from the `sscanf()` result of the supplied string.

* `alloc_full()`
* `linux_parse_cpumap(path)`

> returns a newly-allocated bitmap from a Linux kernel cpumap file

* `cpuset_from_glibc_sched_affinity(bitmask)`

> returns a new bitmap from a list of set bit indexes

#### Operators
These Python operators can be used on bitmap objects:
* `|` (arithmetic 'or')

> creates a new bitmap object using `hwloc_bitmap_or`

* `&` (arithmetic 'and')

> results in a new bitmap object created with `hwloc_bitmap_and`

* `^` (arithmetic 'exclusive or')

> creates a new bimap object from `hwloc_bitmap_xor`

* `!` (arithmetic 'not')

> results in a new bitmap object created with `hwloc_bitmap_not`

* `in`

> `<integer> in bitmap` is True if `hwloc_bitmap_isset` is true for the bitmap and the bit index indicated by the integer.  
   `bitmap1 in bitmap2` is True if `hwloc_bitmap_isincluded(bitmap1, bitmap2)` returns true. That is, if all the bits set in `bitmap1` are set in `bitmap2`

Additionally, a `Bitmap` object can be converted to a string or list. `str(bitmap)` returns the result of `hwloc_bitmap_asprintf` for the bitmap. `tuple(bitmap)` will create tuple consisting of the index numbers of the bits set in `bitmap`.

A `Bitmap` object may be used as a boolean. It is true is `hwloc_bitmap_iszero` returns zero fir the bitmap.

A `Bitmap` object may also be used where an iterator is expected. `for bit in bitmap` will iterate through the indices of the set bits.
The length of a `Bitmap` object is the number of set bits (`hwloc_bitmap_weight`).

`Bitmap` objects may be tested for bitwise equality using the `==` operator. *Note* however that `bitmap1 is bitmap2` is *not* a test of equality. It is only True when both variable names refer to the same bitmap object.

Assignment of a bitmap to another variable only creates another reference to the same object. In order to create a new copy of a bitmap object, you must use the `dup` method. The Python `copy` module's `copy()` function will also make a duplicate.

*Note* that unlike the `copy` method supported by many Python classes, the `Bitmap` class has a `copy` function that follows the `hwloc_bitmap_copy` function. It copies the other bitmap to this bitmap.

#### Properties
Most of the bitmap functions that require no arguments other than the bitmap itself are implemented as properties. A property `<name>` is equivalent to the `hwloc_bitmap_<name>` function.
* `iszero`
* `isfull`
* `first`
* `all_set_bits` -> tuple of `int`
* `last`

*Note* that some functions like `zero`, `fill`, and `weight` are presented as methods rather than properties, to indicate that they may be expensive operations.

#### Methods
A few of the `Bitmap` methods have a slightly different signature that the C library equivalents. They are:

* `alloc(value=None)`

>Without an argument, this behaves like `hwloc_bitmap_alloc`. If a value is supplied as an integer, `hwloc_bitmap_set` is called on the newly-allocated bitmap for the integer supplied. If the value is a string, it is passed to `hwloc_bitmap_sscanf` for the new bitmap.

* `from_ulong(mask, idx=0)`

>There is no separate `hwloc_bitmap_from_ulong` and `hwloc_bitmap_from_ith_ulong`. *Note* that the order of arguments is different from the library routine, so that the idx parameter can be defaulted to `0`.

* `ulong(idx=0)`

>Like `from_ulong`, `ulong` takes an optional index, and there is no separate `hwloc_bitmap_to_ulong` equivalent.

* `set_ulong(idx=0)`

>Same as above but for `hwloc_bitmap_set_ith_ulong`.

The rest of the methods have the same argument in order as the `hwloc_bitmap_*` library routines (except of course the bitmap argument is not supplied). If the method returns a value, the type is specified.

* `dup()` -> `Bitmap`
* `copy(other)`
* `asprintf()` -> `str`
* `sscanf(string)`
* `list_asprintf()` -> `str`
* `list_sscanf(string)`
* `taskset_asprintf()` -> `str`
* `taskset_sscanf(string)`
* `zero()`
* `fill()`
* `only(idx)`
* `allbut(idx)`
* `set(index)`
* `set_range(begin, end)`
* `clr(index)`
* `clr_range(begin, end)`
* `singlify()`
* `isset(index)` -> `bool`
* `next(prev)` -> `int`
* `weight()` -> `int`
* `andnot(other)` -> `Bitmap`
* `intersects(other)` -> `bool`
* `isincluded(super_bitmap)` -> `bool`
* `compare_first(other)` -> `int`
* `compare(other)` -> `int`

### `Obj`
The `Obj` class represents the `hwloc_obj` structure, and has properties corresponding to the structure members. It also has methods matching the library functions that are called with a `hwloc_obj` structure as an argument.

*Important Note About `Obj` Structure References*. 
Only the top-level `Topology` instance holds a reference to the  `hwloc_topology` structure and all of the associated `hwloc_obj` structures, and all of their member structures and their member structures. *You must keep a reference to the `Topology` instance* as long as you are accessing anything the C structure points to. When the reference count for a `Topology` instance goes to zero, `hwloc_topology_destroy` is called for it, and any member objects still around will have invalid references.

An `Obj` object can be converted to a string. The resulting string is essentially all the `infos`, then `hwloc_obj_type_snprintf`, followed by `hwloc_obj_attr_snprintf`. This is mostly useful for debugging.

The test for equality between `Obj` instances is a test to see if they are both physically the same C structure (the structure pointer value is the same).

#### Properties
If the value of the property is not an integer, it's type is listed.

* `type` -> `HWLOC_OBJ_SYSTEM` etc.
* `os_index`
* `name` -> `str`
* `memory` -> `ObjMemory`
* `attr` -> `ObjAttr` or `None`
* `depth`
* `logical_index`
* `os_level`
* `next_cousin` -> `Obj` or `None`
* `prev_cousin` -> `Obj` or `None`
* `parent` -> `Obj` or `None`
* `sibling_rank`
* `next_sibling` -> `Obj` or `None`
* `prev_sibling` -> `Obj` or `None`
* `arity`
* `children` -> list of `Obj`
* `first_child` -> `Obj` or `None`
* `last_child` -> `Obj` or `None`
* `userdata`

>`userdata` is read-write. **Note: only integer values are supported**

* `cpuset` -> `Bitmap` or `None`
* `complete_cpuset` -> `Bitmap` or `None`
* `online_cpuset` -> `Bitmap` or `None`
* `allowed_cpuset` -> `Bitmap` or `None`
* `nodeset` -> `Bitmap` or `None`
* `complete_nodeset` -> `Bitmap` or `None`
* `allowed_nodeset` -> `Bitmap` or `None`
* `distances` -> tuple of `Distances`
* `distances_count`
* `infos` -> tuple of `ObjInfo`
* `infos_count`
* `symmetric_subtree`
* `type_string` -> `str`

>The result of calling `hwloc_obj_type_string` for this object's `type`

* `non_io_ancestor` -> `Obj` or `None` 

#### Class Methods

* `type_of_string(string)` -> the 'type' value returned by `type_sscanf()`
* `type_sscanf(string)` -> (`HWLOC_OBJ_SYSTEM` etc. or `None`, depth or `None`, cache_type or `None`)
* `string_of_type(type enum)` -> `str`
* `cpuset_asprintf(list of Obj)` -> `str` returned by `hwloc_obj_cpuset_snprintf`
* `get_common_ancestor(obj1, obj2)` -> `Obj`

#### Methods

* `type_asprintf(verbose=0)` -> `str`
* `attr_asprintf(separator=`'#'`, verbose=0)` -> `str`
* `get_info_by_name(str)` -> `ObjInfo`
* `add_info(<name> str, <value> str)`
* `get_ancestor_obj_by_depth(int)` -> `Obj` or `None`
* `get_ancestor_obj_by_type(int)` -> `Obj` or `None`
* `get_next_child(<prev> Obj)` -> `Obj`
* `get_common_ancestor_obj(Obj)` -> `Obj`
* `is_in_subtree(<subtree_root> Obj)` -> `bool`
* `get_shared_cache_covering()` -> `Obj` or `None`
* `gl_get_display()` -> `Obj` or `None`

### `ObjMemory`
The `memory` property of an Obj class object is an object of the `ObjMemory` class, corresponding the the `hwloc_obj_memory` structure. It has these properties:

* `total_memory`
* `local_memory` (read-write)
* `page_types` -> tuple of `ObjMemoryPageType`

#### `ObjMemoryPageType`
Corresponding to the `hwloc_obj_memory_page_type` structure, this has two integer properties:

* `size`
* `count`

### `ObjAttr`
The `attr` property of an `Obj` object is an object of `ObjAttr` class. Corresponding o the `hwloc_obj_attr` union, it will return an object instance for one of the following properties:

* `cache` -> `CacheAttr`
* `group` -> `GroupAttr`
* `pcidev` -> `PCIAttr`
* `bridge` -> `BridgeAttr`
* `osdev` -> `OSDevAttr`

>*Note* that like the C union, the result of accessing these through the wrong attribute class is undefined.

#### `CacheAttr`
Like the `hwloc_cache_attr` structure, this class has these integer properties:

* `size`
* `depth`
* `linesize`
* `associativity`
* `type` -> `HWLOC_OBJ_CACHE_UNIFIED` etc.

#### `GroupAttr`
This matches the `hwloc_group_attr` structure, and has this integer property:

* `depth`

#### `PCIDevAttr`
Corresponding to the `hwloc_pcidev_attr` structure, this class has these integer properties:

* `domain`
* `bus`
* `dev`
* `func`
* `class_id`
* `vendor_id`
* `device_id`
* `subvendor_id`
* `subdevice_id`
* `revision`
* `linkspeed`

### `BridgeAttr`
This class represents the `hwloc_bridge_attr` structure.

* `upstream` -> `BridgeAttrUpstream`
* `upstream_type` -> `HWLOC_OBJ_BRIDGE_HOST` etc.
* `downstream` -> `BridgeAttrDownstream`
* `downstream_type` -> `HWLOC_OBJ_BRIDGE_HOST` etc.
* `depth` -> `int`

#### `BridgeAttrUpstream`

* `pci` -> `PCIDevAttr`

#### `BridgeAttrDownstream`
* `pci` -> `BridgeAttrDownstreamPCI`

#### `BridgeAttrDownstreamPCI`

* `domain`
* `seconday_bus`
* `subordinate_bus`

#### `BridgeAttr` example
```python
for obj in topology.bridges:
    assert obj.type == hwloc.OBJ_BRIDGE
    if obj.attr.bridge.upstream_type == hwloc.OBJ_BRIDGE_HOST:
        assert obj.attr.bridge.downstream_type == hwloc.OBJ_BRIDGE_PCI
        print(' Found host->PCI bridge for domain %04x bus %02x-%02x' % (
            obj.attr.bridge.downstream.pci.domain,
            obj.attr.bridge.downstream.pci.secondary_bus,
            obj.attr.bridge.downstream.pci.subordinate_bus))
```

#### Distances
* `relative_depth` -> `int`
* `nbobjs` -> `int`
* `latency` -> tuple of `float`
* `latency_max` -> `float`
* `latency_base` -> `float`

#### ObjInfo
`ObjInfo` represents the `hwloc_obj_info` structure. It can be converted to a `str` type, resulting in `"<name>:<value>"`. It has these properties:

* `name` -> `str`
* `value` -> `str`

### `TopologySupport`
The `support` property of a `Topology` object is an object of the `TopologySupport` class, similar to the `hwloc_topology_support` structure. This class has 3 properties:

* `discovery` -> `TopologyDiscoverySupport`
* `cpubind` -> `TopologyCpubindSupport`
* `membind` ->`TopologyMembindSupport`

All of these objects have properties that are booleans describing what support is available. See the documentation for `hwloc_topology_support` in the `hwloc` package for the meanings of these booleans.

#### `TopologyDiscoverySupport`
This corresponds to the `hwloc_topology_discovery_support` structure. It has this boolean property:

* `pu`

#### TopologyCpubindSupport
This corresponds to the `hwloc_topology_cpubind_support` structure, and has these boolean properties:

* `get_proc_cpubind`
* `get_proc_last_cpu_location`
* `get_thisproc_cpubind`
* `get_thisproc_last_cpu_location`
* `get_thisthread_cpubind`
* `get_thisthread_last_cpu_location`
* `get_thread_cpubind`
* `set_proc_cpubind`
* `set_thisproc_cpubind`
* `set_thisthread_cpubind`
* `set_thread_cpubind`

#### `TopologyMembindSupport`
This corresponds to the `hwloc_topology_membind_support` structure, It has the following boolean properties:

* `set_thisproc_membind`
* `get_thisproc_membind`
* `set_proc_membind`
* `get_proc_membind`
* `set_thisthread_membind`
* `get_thisthread_membind`
* `set_area_membind`
* `get_area_membind`
* `alloc_membind`
* `firsttouch_membind`
* `bind_membind`
* `interleave_membind`
* `replicate_membind`
* `nexttouch_membind`
* `migrate_membind`

#### `TopologyDiff`
Corresponding to the `hwloc_topology_diff` union, it has these properties. Referencing the member structure through the wrong class type has unknown results, except that `type` can always be referenced as though the class was `TopologyDiffGeneric`.

* `type` -> `HWLOC_TOPOLOGY_DIFF_OBJ_ATTR` etc.
* `generic` -> `TopologyDiffGeneric`
* `obj_attr` -> `TopologyDiffObjAttrU`
* `too-complex` -> `TopologyDiffTooComplex`
* `obj_depth` -> `int`
* `obj_index` -> `int`

#### `TopologyDiffGeneric`
* `type` -> `HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_SIZE` etc.
* `next` -> `TopologyDiff` or `None`

#### `TopologyDiffObjAttrUint64`
* `type` -> `HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_SIZE` etc.
* `index` -> `int`
* `oldvalue` -> `int`
* `newvalue` -> `int`

#### `TopologyDiffObjAttrString`
* `type` -> `HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_NAME` etc.
* `name` -> `str`
* `oldvalue` -> `str`
* `newvalue` -> `str`

#### `TopologyDiffTooComplex`
* `type` ->`HWLOC_TOPOLOGY_DIFF_TOO_COMPLEX`
* `next` -> `TopologyDiff` or `None`
* `obj_depth` -> `int`
* `obj_index` -> `int`

#### `TopologyDiffObjAttrU`
* `generic` -> `TopologyDiffObjAttrGeneric`
* `uint64` -> `TopologyDiffObjAttrUint64`
* `string` -> `TopologyDiffObjAttrString`

#### `TopologyDiffObjAttr`
* `type` -> `HWLOC_TOPOLOGY_DIFF_OBJ_ATTR_SIZE` etc.
* `next` -> `TopologyDiff` or `None`
* `obj_depth` -> `int`
* `obj_index` -> `int`
* `diff` -> `TopologyDiffObjAttrU`

### `Topology`
***Note*** You must hold a reference to your `Topology` object as long as you want to reference any constituent part of it

#### General Methods
* `load()`
* `check()`

*Note* there is no `destroy()` method. The topology is destroyed when the Topology instance is no longer referenced.

#### Properties
* `support` -> `TopologySupport`
* `depth` ->`int`
* `is_thissystem` -> `bool`
* `root_obj` -> `Obj`

#### Methods for Configuring Topology Detection
* `ignore_type(int or str)`
* `ignore_type_keep_structure(<int or str>)`

>The two functions above can take a type value or a string recognized by `hwloc_obj_type_sscanf()`

* `ignore_all_keep_structure()`
* `set_flags(flags)`
* `set_pid(pid)`
* `set_fsroot(path)`
* `set_synthetic(string)`
* `set_xml(xmlpath)`
* `set_xmlbuffer(xmlbuffer)`
* `set_custom()`
* `set_distance_matrix(<obj_type> int, <os_index> list of int, <distances> list of int)`

#### Methods for exporting Topologies to XML
* `export_xml(path)`
* `export_xmlbuffer()` -> `str`
* `set_userdata_export_callback(cb)`

>cb is a Python function taking `(reserved, Topology, Obj)` arguments

* `export_obj_userdata(reserved, Obj, <name> str, <buffer> str)`
* `export_obj_userdata_base64(reserved, Obj, <name> str, <buffer> str)`
* `set_userdata_import_callback(cb)`

>cb is a Python function taking `(Topology, Obj, name, buf)` arguments. `name` and `buf` are `str` types

* `export_synthetic(<flags> int)`

See `tests/hwloc_object_userdata.py` in the source-code for an example.

#### Topology Information
* `depth` [property] -> `int`
* `get_type_depth(int)` -> `int`
* `get_depth_type(int)` -> `HWLOC_OBJ_SYSTEM` etc.
* `get_nbobjs_by_depth(int)` -> `int`
* `get_nbobjs_by_type(int)` -> `int`
* `get_flags()` -> `int`
* `is_thissystem` [property] -> `bool`

#### CPU Binding
* `set_cpubind(Bitmap, <flags> int)`
* `get_cpubind(<flags>)` ->`Bitmap`
* `set_proc_cpubind(<pid> int, Bitmap, <flags> int)`
* `get_proc_cpubind(<pid> int, <flags> int)` -> `Bitmap`
* `set_thread_cpubind(<thread> int, Bitmap, <flags> int)`
* `get_thread_cpubind(<thread> int, <flags> int)` -> `Bitmap`
* `get_last_cpu_location(<flags> int)` -> `Bitmap`
* `get_proc_last_cpu_location(<pid> int, <flags> int)` -> `Bitmap`

#### Memory Binding
* `set_membind_nodeset(self, Bitmap, policy, flags)`
* `set_membind(self, Bitmap, policy, flags)`
* `get_membind_nodeset(flags)` -> `Bitmap`
* `get_membind(flags)` -> `Bitmap`
* `set_proc_membind_nodeset(self, pid, Bitmap, policy, flags)`
* `set_proc_membind(pid, Bitmap, policy, flags)`
* `get_proc_membind_nodeset(pid, flags)` -> `Bitmap`
* `get_proc_membind(pid, flags)` -> `Bitmap`
* `set_area_membind_nodeset(addr, length, Bitmap, policy, flags)`
* `set_area_membind(addr, length, Bitmap, policy, flags)`
* `get_area_membind_nodeset(addr, length, flags)` -> `Bitmap`
* `get_area_membind(addr, length, flags)` -> `Bitmap`
* `get_area_memlocation(addr, length, flags)` -> `Bitmap`
* `alloc(length)` -> address or `None`
* `alloc_membind_nodeset(length, Bitmap, policy, flags)` -> address or `None`
* `alloc_membind(length, Bitmap, policy, flags)` -> address or `None`
* `alloc_membind_policy_nodeset(len, Bitmap, policy, flags)` -> address or `None`
* `alloc_membind_policy(len, Bitmap, policy, flags)` -> address or `None`
* `free(address, length)`


An example of using the memory methods:
```python
#!/usr/bin/python3
LEN = 1048576

import hwloc, sys, ctypes

topology = hwloc.Topology()
topology.load()

buffer_ = topology.alloc(LEN)
assert buffer_
print('buffer 0x{:X} length {:d}'.format(buffer_, LEN))

if topology.support.membind.get_area_memlocation:
    set_ = topology.get_area_memlocation(buffer_, LEN, hwloc.MEMBIND_BYNODESET)
    print('address 0x{:X} length {:d} allocated in nodeset'.format(buffer_, LEN), str(set_))

# touch the memory
buf = ctypes.cast(buffer_, ctypes.POINTER(ctypes.c_ubyte))
buf[0] = 0
buf[LEN-1] = 0 

topology.free(buffer_, LEN)
```

#### Modifying A Loaded Topology

* `insert_misc_object_by_cpuset(<cpuset> Bitmap, name)` -> `Obj`
* `insert_misc_object_by_parent(<parent> Obj, name)` -> `Obj`
* `restrict(Bitmap, flags=0)`
* `dup()` -> `Topology`

#### Building Custom Topologies

* `custom_insert_topology(<newparent> Obj, <oldtopology> Topology, <oldroot> Obj=None)`
* `custom_insert_group_object_by_parent(<parent> Obj, groupdepth)` -> `Obj`

#### Object Type Helpers

* `get_type_or_below_depth(type)` -> `int`
* `get_type_or_above_depth(type)` -> `int`

#### Retrieve Objects

* `get_obj_by_depth(depth, index)` -> `Obj` or `None`
* `get_obj_by_type(type, index)` -> `Obj` or `None`

#### Object/String Conversion

* `obj_asprintf(Obj, prefix, verbose=0)` -> `str`

#### Basic Traversal Helpers

* `root_obj` [property] -> `Obj`
* `get_next_obj_by_depth(depth, <prev> Obj=None)` -> `Obj` or `None`
* `objs_by_depth(depth, <prev> Obj=None)` -> generator object yielding `Obj`
* `get_next_obj_by_type(type, <prev> Obj=None)` -> `Obj` or `None`
* `objs_by_type(type, <prev> Obj=None)` -> generator object yielding `Obj`
* `obj_is_in_subtree(self, Obj, <subtree_root> Obj)` -> bool

#### Finding Objects Inside a CPU set

* `get_first_largest_obj_inside_cpuset(Bitmap)` -> `Obj` or `None
* `get_largest_objs_inside_cpuset(Bitmap, max)` -> tuple of Obj, or ArgError exception
* `get_next_obj_inside_cpuset_by_depth(Bitmap, depth, <prev> Obj=None)` -> `Obj` or `None`
* `objs_inside_cpuset_by_depth(Bitmap, depth, <prev> Obj=None)` -> generator object yielding `Obj`
* `get_next_obj_inside_cpuset_by_type(Bitmap, type, <prev> Obj=None)` -> `Obj` or `None`
* `objs_inside_cpuset_by_type(Bitmap, type, <prev> Obj=None)` -> generator object yielding `Obj`
* `get_obj_inside_cpuset_by_depth(Bitmap, depth, idx)` -> `Obj` or `None`
* `get_obj_inside_cpuset_by_type(Bitmap, type, idx)` -> `Obj` or `None`
* `get_nbobjs_inside_cpuset_by_depth(Bitmap, depth)`
* `get_nbobjs_inside_cpuset_by_type(bitmap, type)`
* `get_obj_index_inside_cpuset(Bitmap, Obj)`

#### Finding a single Object covering at least a CPU set

* `get_child_covering_cpuset(Bitmap, <parent> Obj) -> `Obj` or `None`
* `get_obj_covering_cpuset(Bitmap)` -> `Obj` or `None`
* `get_next_obj_covering_cpuset_by_depth(Bitmap, depth, <prev> Obj=None)` -> `Obj` or `None`
* `objs_covering_cpuset_by_depth(Bitmap, depth, <prev> Obj=None)` -> generator object yielding `Obj`
* `get_next_obj_covering_cpuset_by_type(Bitmap, type, <prev> Obj=None)` -> `Obj` or `None`
* `objs_covering_cpuset_by_type(Bitmap, type, <prev> Obj=None) -> generator object yielding `Obj`

Example usage:
```python
#!/usr/bin/env python3
import hwloc

topo = hwloc.Topology()

set1 = hwloc.Bitmap.alloc('00008f18')

topo.set_synthetic('nodes:8 cores:2 1')
topo.load()

obj = topo.get_next_obj_covering_cpuset_by_type(set1, hwloc.OBJ_NODE, None)
assert obj == topo.get_obj_by_depth(1, 1)

topo = hwloc.Topology()
topo.set_synthetic('nodes:2 socket:5 cores:3 4')
topo.load()

set1.sscanf('0ff08000')

depth = topo.get_type_depth(hwloc.OBJ_SOCKET)
assert depth == 2

for index, obj in enumerate(topo.objs_covering_cpuset_by_depth(set1, depth),
                            start=1):
    assert obj == topo.get_obj_by_depth(depth, index)
```

#### Cache-specific Finding Helpers

* `get_cache_type_depth(<cachelevel> int, <cachetype> int)` -> `int`
* `get_cache_covering_cpuset(Bitmap)` -> `Obj` or `None`
* `get_shared_cache_covering_obj(Obj)` -> `Obj` or `None`

#### inding objects, miscellaneous helpers

* `get_pu_obj_by_os_index(os_index)` -> `Obj` or `None`
* `get_numanode_obj_by_os_index(os_index)` -> `Obj` or `None`
* `get_closest_objs(Obj, max)` -> tuple of `Obj`
* `get_obj_below_by_type(type1, idx1, type2, idx2)` -> `Obj` or `None`
* `get_obj_below_array_by_type((type, idx), ... )` -> `Obj` or `None`

An example of `get_obj_below_array_by_type`:
```python
#!/usr/bin/env python3
import hwloc

topo = hwloc.Topology()

topo.set_synthetic('node:3 pack:3 core:3 pu:3')

topo.load()

# find the first thread
obj = topo.get_obj_below_array_by_type((hwloc.OBJ_NODE, 0),
                                       (hwloc.OBJ_SOCKET, 0),
                                       (hwloc.OBJ_CORE, 0),
                                       (hwloc.OBJ_PU, 0))
assert obj == topo.get_obj_by_depth(4, 0)

# find the last core
obj = topo.get_obj_below_array_by_type((hwloc.OBJ_NODE, 2),
                                       (hwloc.OBJ_SOCKET, 2),
                                       (hwloc.OBJ_CORE, 2))
assert obj == topo.get_obj_by_depth(3, 26)
```

#### Distributing items over a topology

* ` distrib(<roots> list of OBJ, n, until, flags=0)` -> tuple of n Bitmap objects

> `distribute` and `distributev` are deprecated

#### Cpuset Helpers

* `complete_cpuset` [property] -> `Bitmap`
* `cpuset` [property] -> `Bitmap`
* `online_cpuset` [property] -> `Bitmap`
* `allowed_cpuset` [property] -> `Bitmap`

#### Nodeset Helpers

* `complete_nodeset` [property] -> `Bitmap`
* `nodeset` [property] -> `Bitmap`
* `allowed_nodeset` [property] -> `Bitmap`

#### Converting between CPU sets and node sets

* `cpuset_to_nodeset(Bitmap)` -> `Bitmap`
* `cpuset_to_nodeset_strict(Bitmap)` -> `Bitmap`
* `cpuset_from_nodeset(Bitmap)` -> `Bitmap`
* `cpuset_from_nodeset_strict(Bitmap)` -> `Bitmap`

#### Manipulating Distances

* `get_whole_distance_matrix_by_depth(depth)` -> `Distances` or `None`
* `get_whole_distance_matrix_by_type(type)` -> `Distances` or `None`
* `get_distance_matrix_covering_obj_by_depth(Obj, depth)` -> `Distances` or `None`
* `get_latency(Obj, Obj)` -> (<latency> `float`, <reverse_latency> `float`)

#### Finding I/O objects

* `get_non_io_ancestor_obj(Obj)` -> `Obj` or `None`
* `get_next_pcidev(Obj)` -> `Obj` or `None`
* `pcidevs` [property] -> generator object yielding `Obj`
* `get_pcidev_by_busid(<domain> str, <bus> str, <dev> str, <func> str)` -> `Obj` or `None`
* `get_pcidev_by_busidstring(<busid> str)` -> `Obj` or `None`
* `get_next_osdev(<prev> Obj)` -> `Obj` or `None`
* `osdevs` [property] -> generator object yielding `Obj`
* `get_next_bridge(<prev> Obj)` -> `Obj` or `None`
* `bridges` [property] -> generator object yielding Obj
* `bridge_covers_pcibus(<domain> str, <bus> str)` -> `bool`
* `get_hostbridge_by_pcibus(<domain> str, <bus> str)` -> `Obj` or `None`

See the `BridgeAttr` section for an example.

#### Topology differences

* `diff_build(<newtopology> Topology, flags=0)` -> (`TopologyDiff` or `None`, \<toocomplex> bool)
* `diff_apply(TopologyDiff, flags=0)`
* `diff_load_xml(<xmlpath> str)` -> (`TopologyDiff`, <refname> `str`)
* `diff_export_xml(TopologyDiff, <refname> str, <xmlpath> str)`
* `diff_load_xmlbuffer(str)` -> (`TopologyDiff`, <refname> `str`)
* `diff_export_xmlbuffer(Topologydiff, <refname> str=None)` -> \<xmlbuffer> `str`

#### Linux-only helpers

* `linux_set_tid_cpubind(tid, Bitmap)`
* `linux_get_tid_cpubind(tid)` -> `Bitmap`
* `linux_get_tid_last_cpu_location(tid)` -> `Bitmap`

#### OpenGL display specific functions

* `gl_get_display_osdev_by_port_device(<port> int, <device> int)` -> `Obj`
* `gl_get_display_osdev_by_name(str)` -> `Obj`
* `gl_get_display_by_osdev(Obj)` -> `int`

#### Helpers for manipulating Linux libnuma unsigned long masks

* `cpuset_to_linux_libnuma_ulongs(Bitmap)` -> (tuple of `int`, \<maxnode> `int`)
* `nodeset_to_linux_libnuma_ulongs(Bitmap)` -> (tuple of `int`, \<maxnode> `int`)
* `cpuset_from_linux_libnuma_ulongs(list of `int`, <maxnode> int=None)` -> `Bitmap`
* `nodeset_from_linux_libnuma_ulongs(list of `int`, <maxnode> int=None)` -> `Bitmap`
* `cpuset_to_linux_libnuma_bitmask(Bitmap)` -> `libnuma.Bitmask()`
* `nodeset_to_linux_libnuma_bitmask(Bitmap)` -> `libnuma.Bitmask()`
* `cpuset_from_linux_libnuma_bitmask(libnuma.Bitmask)` -> `Bitmap`
* `nodeset_from_linux_libnuma_bitmask(libnuma.Bitmask)` -> `Bitmap`

#### Intel Xeon Phi (MIC) Specific Functions

* `intel_mic_get_device_cpuset(int)` -> Bitmap
* `intel_mic_get_device_osdev_by_index(int)` -> `Obj`
* `intel_mic_device_osdevs` [property] -> generator object yielding `Obj`

## Module-Level Functions

* `compare_types(<type1> int or str, <type2> int or str)` -> int

> `compare_types()` can take a type constant or a string recognized by `hwloc_obj_type_sscanf()`
* `get_api_version`()` -> `int`
* `version_string()` -> `str`
* `cpuset_from_glibc_sched_affinity(list of set bit indexes)` -> `Bitmap`

## Constants

* `Version` -> `int`
* `INT_MAX` -> `int`
* `UINT_MAX` -> `int`
