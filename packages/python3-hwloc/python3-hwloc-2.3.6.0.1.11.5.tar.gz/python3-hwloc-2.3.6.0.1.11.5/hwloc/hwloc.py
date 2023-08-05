# -*- python -*-
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

__author = 'Guy Streeter <guy.streeter@gmail.com>'
__license = 'GPLv2'
__version = '2.3-1.11.5'
__description = 'Python bindings for hwloc'
__URL = 'https://gitlab.com/guystreeter/python-hwloc'

from . import chwloc as C


INT_MAX = C.HWLOC_INT_MAX
UINT_MAX = C.HWLOC_UINT_MAX

OBJ_SYSTEM = C.OBJ_SYSTEM
OBJ_MACHINE = C.OBJ_MACHINE
OBJ_NUMANODE = C.OBJ_NUMANODE
OBJ_PACAGE = C.OBJ_PACKAGE
OBJ_NODE = C.OBJ_NODE
OBJ_SOCKET = C.OBJ_SOCKET
OBJ_CACHE = C.OBJ_CACHE
OBJ_CORE = C.OBJ_CORE
OBJ_PU = C.OBJ_PU
OBJ_GROUP = C.OBJ_GROUP
OBJ_MISC = C.OBJ_MISC
OBJ_BRIDGE = C.OBJ_BRIDGE
OBJ_PCI_DEVICE = C.OBJ_PCI_DEVICE
OBJ_OS_DEVICE = C.OBJ_OS_DEVICE
OBJ_TYPE_MAX = C.OBJ_TYPE_MAX

OBJ_CACHE_UNIFIED = C.OBJ_CACHE_UNIFIED
OBJ_CACHE_DATA = C.OBJ_CACHE_DATA
OBJ_CACHE_INSTRUCTION = C.OBJ_CACHE_INSTRUCTION

OBJ_BRIDGE_HOST = C.OBJ_BRIDGE_HOST
OBJ_BRIDGE_PCI = C.OBJ_BRIDGE_PCI

OBJ_OSDEV_BLOCK = C.OBJ_OSDEV_BLOCK
OBJ_OSDEV_GPU = C.OBJ_OSDEV_GPU
OBJ_OSDEV_NETWORK = C.OBJ_OSDEV_NETWORK
OBJ_OSDEV_OPENFABRICS = C.OBJ_OSDEV_OPENFABRICS
OBJ_OSDEV_DMA = C.OBJ_OSDEV_DMA
OBJ_OSDEV_COPROC = C.OBJ_OSDEV_COPROC

TYPE_UNORDERED = C.TYPE_UNORDERED

TOPOLOGY_FLAG_WHOLE_SYSTEM = C.TOPOLOGY_FLAG_WHOLE_SYSTEM
TOPOLOGY_FLAG_IS_THISSYSTEM = C.TOPOLOGY_FLAG_IS_THISSYSTEM
TOPOLOGY_FLAG_IO_DEVICES = C.TOPOLOGY_FLAG_IO_DEVICES
TOPOLOGY_FLAG_IO_BRIDGES = C.TOPOLOGY_FLAG_IO_BRIDGES
TOPOLOGY_FLAG_WHOLE_IO = C.TOPOLOGY_FLAG_WHOLE_IO
TOPOLOGY_FLAG_ICACHES = C.TOPOLOGY_FLAG_ICACHES

RESTRICT_FLAG_ADAPT_DISTANCES = C.RESTRICT_FLAG_ADAPT_DISTANCES
RESTRICT_FLAG_ADAPT_MISC = C.RESTRICT_FLAG_ADAPT_MISC
RESTRICT_FLAG_ADAPT_IO = C.RESTRICT_FLAG_ADAPT_IO

TYPE_DEPTH_UNKNOWN = C.TYPE_DEPTH_UNKNOWN
TYPE_DEPTH_MULTIPLE = C.TYPE_DEPTH_MULTIPLE
TYPE_DEPTH_BRIDGE = C.TYPE_DEPTH_BRIDGE
TYPE_DEPTH_PCI_DEVICE = C.TYPE_DEPTH_PCI_DEVICE
TYPE_DEPTH_OS_DEVICE = C.TYPE_DEPTH_OS_DEVICE

CPUBIND_PROCESS = C.CPUBIND_PROCESS
CPUBIND_THREAD = C.CPUBIND_THREAD
CPUBIND_STRICT = C.CPUBIND_STRICT
CPUBIND_NOMEMBIND = C.CPUBIND_NOMEMBIND

MEMBIND_DEFAULT = C.MEMBIND_DEFAULT
MEMBIND_FIRSTTOUCH = C.MEMBIND_FIRSTTOUCH
MEMBIND_BIND = C.MEMBIND_BIND
MEMBIND_INTERLEAVE = C.MEMBIND_INTERLEAVE
MEMBIND_REPLICATE = C.MEMBIND_REPLICATE
MEMBIND_NEXTTOUCH = C.MEMBIND_NEXTTOUCH
MEMBIND_MIXED = C.MEMBIND_MIXED

MEMBIND_PROCESS = C.MEMBIND_PROCESS
MEMBIND_THREAD = C.MEMBIND_THREAD
MEMBIND_STRICT = C.MEMBIND_STRICT
MEMBIND_MIGRATE = C.MEMBIND_MIGRATE
MEMBIND_NOCPUBIND = C.MEMBIND_NOCPUBIND
MEMBIND_BYNODESET = C.MEMBIND_BYNODESET

TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_EXTENDED_TYPES = C.TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_EXTENDED_TYPES
TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_ATTRS = C.TOPOLOGY_EXPORT_SYNTHETIC_FLAG_NO_ATTRS

TOPOLOGY_DIFF_OBJ_ATTR_SIZE = C.TOPOLOGY_DIFF_OBJ_ATTR_SIZE
TOPOLOGY_DIFF_OBJ_ATTR_NAME = C.TOPOLOGY_DIFF_OBJ_ATTR_NAME
TOPOLOGY_DIFF_OBJ_ATTR_INFO = C.TOPOLOGY_DIFF_OBJ_ATTR_INFO

TOPOLOGY_DIFF_OBJ_ATTR = C.TOPOLOGY_DIFF_OBJ_ATTR
TOPOLOGY_DIFF_TOO_COMPLEX = C.TOPOLOGY_DIFF_TOO_COMPLEX

TOPOLOGY_DIFF_APPLY_REVERSE = C.TOPOLOGY_DIFF_APPLY_REVERSE

# Linux-only stuff, shouldn't be invoked elsewhere
try:
    import linuxsched
except:
    pass


def _unfate(text):
    if isinstance(text, bytes):
        return text.decode('utf8')
    raise ValueError('requires text input, got %s' % type(text))


class Error(Exception):
    pass


class ArgError(Error):
    """Exception raised when a calling argument is invalid"""

    def __init__(self, string):
        self.msg = string

    def __str__(self):
        return self.msg


Version = C.get_api_version()
get_api_version = C.get_api_version


def version_string():
    v = get_api_version()
    major = v >> 16
    minor = (v >> 8) & 0xFF
    rev = v & 0xFF
    s = '%u' % major
    if minor or rev:
        s += '.%u' % minor
    if rev:
        s += '.%u' % rev
    return s


class TopologyDiscoverySupport(object):
    """booleans describing actual discovery support for this topology"""

    def __init__(self, tds_ptr):
        self._tds = tds_ptr

    @property
    def pu(self):
        return self._tds.pu


class TopologyCpubindSupport(object):
    """booleans describing support for cpu binding"""

    def __init__(self, cpubs_ptr):
        self._cpubs_ptr = cpubs_ptr

    @property
    def set_thisproc_cpubind(self):
        return bool(self._cpubs_ptr.set_thisproc_cpubind)

    @property
    def get_thisproc_cpubind(self):
        return bool(self._cpubs_ptr.get_thisproc_cpubind)

    @property
    def set_proc_cpubind(self):
        return bool(self._cpubs_ptr.set_proc_cpubind)

    @property
    def get_proc_cpubind(self):
        return bool(self._cpubs_ptr.get_proc_cpubind)

    @property
    def set_thisthread_cpubind(self):
        return bool(self._cpubs_ptr.set_thisthread_cpubind)

    @property
    def get_thisthread_cpubind(self):
        return bool(self._cpubs_ptr.get_thisthread_cpubind)

    @property
    def set_thread_cpubind(self):
        return bool(self._cpubs_ptr.set_thread_cpubind)

    @property
    def get_thread_cpubind(self):
        return bool(self._cpubs_ptr.get_thread_cpubind)

    @property
    def get_thisproc_last_cpu_location(self):
        return bool(self._cpubs_ptr.get_thisproc_last_cpu_location)

    @property
    def get_proc_last_cpu_location(self):
        return bool(self._cpubs_ptr.get_proc_last_cpu_location)

    @property
    def get_thisthread_last_cpu_location(self):
        return bool(self._cpubs_ptr.get_thisthread_last_cpu_location)


class TopologyMembindSupport(object):
    """booleans describing support for memory binding"""

    def __init__(self, mbs_ptr):
        self._mbs_ptr = mbs_ptr

    @property
    def set_thisproc_membind(self):
        return bool(self._mbs_ptr.set_thisproc_membind)

    @property
    def get_thisproc_membind(self):
        return bool(self._mbs_ptr.get_thisproc_membind)

    @property
    def set_proc_membind(self):
        return bool(self._mbs_ptr.set_proc_membind)

    @property
    def get_proc_membind(self):
        return bool(self._mbs_ptr.get_proc_membind)

    @property
    def set_thisthread_membind(self):
        return bool(self._mbs_ptr.set_thisthread_membind)

    @property
    def get_thisthread_membind(self):
        return bool(self._mbs_ptr.get_thisthread_membind)

    @property
    def set_area_membind(self):
        return bool(self._mbs_ptr.set_area_membind)

    @property
    def get_area_membind(self):
        return bool(self._mbs_ptr.get_area_membind)

    @property
    def alloc_membind(self):
        return bool(self._mbs_ptr.alloc_membind)

    @property
    def firsttouch_membind(self):
        return bool(self._mbs_ptr.firsttouch_membind)

    @property
    def bind_membind(self):
        return bool(self._mbs_ptr.bind_membind)

    @property
    def interleave_membind(self):
        return bool(self._mbs_ptr.interleave_membind)

    @property
    def replicate_membind(self):
        return bool(self._mbs_ptr.replicate_membind)

    @property
    def nexttouch_membind(self):
        return bool(self._mbs_ptr.nexttouch_membind)

    @property
    def migrate_membind(self):
        return bool(self._mbs_ptr.migrate_membind)

    @property
    def get_area_memlocation(self):
        return bool(self._mbs_ptr.get_area_memlocation)


class TopologySupport(object):
    """pointers to the support structures"""

    def __init__(self, ts_ptr):
        self._support = ts_ptr

    @property
    def discovery(self):
        return TopologyDiscoverySupport(self._support.discovery)

    @property
    def cpubind(self):
        return TopologyCpubindSupport(self._support.cpubind)

    @property
    def membind(self):
        return TopologyMembindSupport(self._support.membind)


class ObjMemoryPageType(object):

    def __init__(self, ompt_ptr):
        self._page_type = ompt_ptr

    @property
    def size(self):
        return self._page_type.size

    @property
    def count(self):
        return self._page_type.count


class ObjMemory(object):

    def __init__(self, memory_ptr):
        self._memory = memory_ptr

    @property
    def total_memory(self):
        return self._memory.total_memory

    @property
    def local_memory(self):
        return self._memory.local_memory

    @local_memory.setter
    def local_memory(self, value):
        self._memory.local_memory = value

    @property
    def page_types(self):
        p = []
        for t in self._memory.page_types:
            p.append(ObjMemoryPageType(t))
        return tuple(p)


class CacheAttr(object):

    def __init__(self, cache_ptr):
        self._cache = cache_ptr

    @property
    def size(self):
        return self._cache.size

    @property
    def depth(self):
        return self._cache.depth

    @property
    def linesize(self):
        return self._cache.linesize

    @property
    def associativity(self):
        return self._cache.associativity

    @property
    def type(self):
        return self._cache.type


class GroupAttr(object):

    def __init__(self, group_ptr):
        self._group = group_ptr

    @property
    def depth(self):
        return self._group.depth


class PCIDevAttr(object):

    def __init__(self, pcidev_ptr):
        self._pcidev = pcidev_ptr

    @property
    def domain(self):
        return self._pcidev.domain

    @property
    def bus(self):
        return self._pcidev.bus

    @property
    def dev(self):
        return self._pcidev.dev

    @property
    def func(self):
        return self._pcidev.func

    @property
    def class_id(self):
        return self._pcidev.class_id

    @property
    def vendor_id(self):
        return self._pcidev.vendor_id

    @property
    def device_id(self):
        return self._pcidev.device_id

    @property
    def subvendor_id(self):
        return self._pcidev.subvendor_id

    @property
    def subdevice_id(self):
        return self._pcidev.subdevice_id

    @property
    def revision(self):
        return self._pcidev.revision

    @property
    def linkspeed(self):
        return self._pcidev.linkspeed


class BridgeAttrUpstream(object):

    def __init__(self, upstream_ptr):
        self._upstream = upstream_ptr

    @property
    def pci(self):
        return PCIDevAttr(self._upstream.pci)


class BridgeAttrDownstream(object):

    def __init__(self, downstream):
        self._downstream = downstream

    @property
    def pci(self):
        return BridgeAttrDownstreamPCI(self._downstream.pci)


class BridgeAttrDownstreamPCI(object):

    def __init__(self, pci):
        self._pci = pci

    @property
    def domain(self):
        return self._pci.domain

    @property
    def secondary_bus(self):
        return self._pci.secondary_bus

    @property
    def subordinate_bus(self):
        return self._pci.subordinate_bus


class BridgeAttr(object):

    def __init__(self, bridge_ptr):
        self._bridge = bridge_ptr

    @property
    def upstream(self):
        return BridgeAttrUpstream(self._bridge.upstream)

    @property
    def upstream_type(self):
        return self._bridge.upstream_type

    @property
    def downstream(self):
        return BridgeAttrDownstream(self._bridge.downstream)

    @property
    def downstream_type(self):
        return self._bridge.downstream_type

    @property
    def depth(self):
        return self._bridge.depth


class OSDevAttr(object):

    def __init__(self, osdev):
        self._osdev = osdev

    @property
    def type(self):
        return self._osdev.type


class ObjAttr(object):

    def __init__(self, attr_ptr):
        self._objattr = attr_ptr

    @property
    def cache(self):
        return CacheAttr(self._objattr.cache)

    @property
    def group(self):
        return GroupAttr(self._objattr.group)

    @property
    def pcidev(self):
        return PCIDevAttr(self._objattr.pcidev)

    @property
    def bridge(self):
        return BridgeAttr(self._objattr.bridge)

    @property
    def osdev(self):
        return OSDevAttr(self._objattr.osdev)


class Bitmap(object):
    """python object representing the library's internal bitmap structure"""

    def __init__(self, bmp_ptr=None):
        if bmp_ptr is None:
            self._bitmap = C.bitmap_alloc()
            return
        if isinstance(bmp_ptr, Bitmap):
            self._bitmap = C.bitmap_alloc()
            self.copy(bmp_ptr)
            return
        self._bitmap = bmp_ptr

    @classmethod
    def alloc(cls, value=None):
        """returns a newly-allocated bitmap structure"""
        bitmap = Bitmap(C.bitmap_alloc())
        if value is not None:
            try:
                bitmap.set(value)
            except ValueError:
                bitmap.sscanf(value)
        return bitmap

    @classmethod
    def alloc_full(cls):
        return Bitmap(C.bitmap_alloc_full())

    def dup(self):
        return Bitmap(C.bitmap_dup(self._bitmap))

    def copy(self, other):
        """copy other bitmap to this"""
        C.bitmap_copy(self._bitmap, other._bitmap)

    def __copy__(self):
        return self.dup()

    def asprintf(self):
        """returns a string representing the bitmap's values"""
        return C.bitmap_asprintf(self._bitmap)

    def __str__(self):
        return self.asprintf()

    def sscanf(self, string):
        """Set the bitmap's value from a string"""
        try:
            C.bitmap_sscanf(self._bitmap, string)
        except C.ArgError:
            raise ArgError('Bitmap.sscanf() error scanning ' + string)

    def list_asprintf(self):
        """Stringify a bitmap into a newly allocated list string"""
        return C.bitmap_list_asprintf(self._bitmap)

    def list_sscanf(self, string):
        """Parse a string and store it in bitmap"""
        try:
            C.bitmap_list_sscanf(self._bitmap, string)
        except C.ArgError:
            raise ArgError('Bitmap.list_sscanf() error scanning ' + string)

    def taskset_asprintf(self):
        """Stringify a bitmap into a newly allocated taskset-specific string"""
        return C.bitmap_taskset_asprintf(self._bitmap)

    def taskset_sscanf(self, string):
        """Parse a taskset-specific bitmap string and store it in bitmap"""
        return C.bitmap_taskset_sscanf(self._bitmap, string)

    def zero(self):
        C.bitmap_zero(self._bitmap)

    def fill(self):
        C.bitmap_fill(self._bitmap)

    def only(self, idx):
        C.bitmap_only(self._bitmap, idx)

    def allbut(self, idx):
        C.bitmap_allbut(self._bitmap, idx)

    def from_ulong(self, mask, idx=0):
        """Setup bitmap from unsigned long mask used as i-th (defaults to zero) subset"""
        C.bitmap_from_ith_ulong(self._bitmap, idx, mask)

    def set(self, index):
        """Set one index or all the indices in a tuple"""
        try:
            for i in index:
                C.bitmap_set(self._bitmap, i)
        except TypeError:
            C.bitmap_set(self._bitmap, index)

    def set_range(self, begin, end):
        C.bitmap_set_range(self._bitmap, begin, end)

    def set_ulong(self, mask, idx=0):
        """Replace i-th (defaults to zero) subset of bitmap with unsigned long mask"""
        C.bitmap_set_ith_ulong(self._bitmap, idx, mask)

    def clr(self, index):
        C.bitmap_clr(self._bitmap, index)

    def clr_range(self, begin, end):
        C.bitmap_clr_range(self._bitmap, begin, end)

    def singlify(self):
        C.bitmap_singlify(self._bitmap)

    def ulong(self, idx=0):
        """the i-th (defaults to zero) subset of bitmap as an unsigned long mask"""
        return C.bitmap_to_ith_ulong(self._bitmap, idx)

    def isset(self, index):
        return bool(C.bitmap_isset(self._bitmap, index))

    @property
    def iszero(self):
        return bool(C.bitmap_iszero(self._bitmap))

    @property
    def isfull(self):
        return bool(C.bitmap_isfull(self._bitmap))

    @property
    def first(self):
        """index of the first set bit"""
        return C.bitmap_first(self._bitmap)

    def next(self, prev):
        """index of the next set bit"""
        return C.bitmap_next(self._bitmap, prev)

    def __iter__(self):
        """iterator object representing the indices of all the set bits"""
        prev = self.first
        while prev != -1:
            yield prev
            prev = self.next(prev)

    @property
    def all_set_bits(self):
        """tuple of the indices of the set bits"""
        return tuple([x for x in self])

    @property
    def last(self):
        """index of the last set bit"""
        return C.bitmap_last(self._bitmap)

    # not a property, just because it can be an expensive operation
    def weight(self):
        return C.bitmap_weight(self._bitmap)

    def __len(self):
        return self.weight()

    def __or__(self, other):
        newset = Bitmap.alloc()
        C.bitmap_or(newset._bitmap, self._bitmap, other._bitmap)
        return newset

    def __ior__(self, other):
        C.bitmap_or(self._bitmap, self._bitmap, other._bitmap)
        return self

    def __and__(self, other):
        newset = Bitmap.alloc()
        C.bitmap_and(newset._bitmap, self._bitmap, other._bitmap)
        return newset

    def __iand__(self, other):
        C.bitmap_and(self._bitmap, self._bitmap, other._bitmap)
        return self

    def __bool__(self):
        return self.iszero

    def __nonzero__(self):
        return not self.iszero

    def andnot(self, other):
        """returns a new bitmap representing "and not" of this and the other bitmap"""
        new = Bitmap.alloc()
        try:
            C.bitmap_andnot(new._bitmap, self._bitmap, other._bitmap)
        except TypeError:
            C.bitmap_andnot(new._bitmap, self._bitmap,
                            Bitmap.alloc(other)._bitmap)
        return new

    def __xor__(self, other):
        newset = Bitmap.alloc()
        C.bitmap_xor(newset._bitmap, self._bitmap, other._bitmap)
        return newset

    def __ixor__(self, other):
        C.bitmap_xor(self._bitmap, self._bitmap, other._bitmap)

    def __invert__(self):
        """bitwise not"""
        newset = Bitmap.alloc()
        C.bitmap_not(newset._bitmap, self._bitmap)
        return newset

    def intersects(self, other):
        """True if the two bitmaps have any set bit in common"""
        return bool(C.bitmap_intersects(self._bitmap, other._bitmap))

    def isincluded(self, super_bitmap):
        """True if this bitmap is part of super_bitmap"""
        return bool(C.bitmap_isincluded(self._bitmap, super_bitmap._bitmap))

    def __contains__(self, other):
        """"other" can be an int index or a bitmap"""
        if isinstance(other, int):
            return self.isset(other)
        # "sub_bitmap in super_bitmap" is sub_bitmap.isincluded(super_bitmap)
        # and super_bitmap is this bitmap (self)
        return other.isincluded(self)

    def __eq__(self, other):
        return bool(C.bitmap_isequal(self._bitmap, other._bitmap))

    def __ne__(self, other):
        return not self == other

    def compare_first(self, other):
        """Compare bitmaps using their lowest index"""
        return C.bitmap_compare_first(self._bitmap, other._bitmap)

    def compare(self, other):
        return C.bitmap_compare(self._bitmap, other._bitmap)

    # helpers
    @classmethod
    def linux_parse_cpumap(cls, path):
        """Convert a linux kernel cpumap file into hwloc CPU set
        returns a newly-allocated bitmap"""
        return Bitmap(C.linux_parse_cpumap(path))

    def to_glibc_sched_affinity(self):
        """get a glibc-style cpuset equivalent to this bitmap"""
        cpuset = linuxsched.cpu_set_t()
        for i in self.all_set_bits:
            cpuset.CPU_SET(i)
        return cpuset


def cpuset_from_glibc_sched_affinity(bitmask):
    """return a Bitmap equivalent to the supplied glibc-style cpuset"""
    cpuset = Bitmap.alloc()
    for i in bitmask:
        cpuset.set(i)
    return cpuset


class ObjInfo(object):

    def __init__(self, info_ptr):
        self._info = info_ptr

    @property
    def name(self):
        return _unfate(self._info.name)

    @property
    def value(self):
        return _unfate(self._info.value)

    def __str__(self):
        return self.name + ':' + self.value


class Distances(object):

    def __init__(self, dist_ptr):
        self._dist = dist_ptr

    @property
    def relative_depth(self):
        return self._dist.relative_depth

    @property
    def nbobjs(self):
        return self._dist.nbobjs

    @property
    def latency(self):
        return tuple(self._dist.latency[:])

    @property
    def latency_max(self):
        return self._dist.latency_max

    @property
    def latency_base(self):
        return self._dist.latency_base


class Obj(object):

    def __init__(self, obj_ptr):
        self._obj = obj_ptr

    @property
    def type(self):
        return self._obj.type

    @property
    def os_index(self):
        return self._obj.os_index

    @property
    def name(self):
        if self._obj.name is None:
            return None
        return _unfate(self._obj.name)

    @property
    def memory(self):
        return ObjMemory(self._obj.memory)

    @property
    def attr(self):
        try:
            return ObjAttr(self._obj.attr)
        except C.NULLError:
            return None

    @property
    def depth(self):
        return self._obj.depth

    @property
    def logical_index(self):
        return self._obj.logical_index

    @property
    def os_level(self):
        return self._obj.os_level

    @property
    def next_cousin(self):
        try:
            return Obj(self._obj.next_cousin)
        except C.NULLError:
            return None

    @property
    def prev_cousin(self):
        try:
            return Obj(self._obj.prev_cousin)
        except C.NULLError:
            return None

    @property
    def parent(self):
        try:
            return Obj(self._obj.parent)
        except C.NULLError:
            return None

    @property
    def sibling_rank(self):
        return self._obj.sibling_rank

    @property
    def next_sibling(self):
        try:
            return Obj(self._obj.next_sibling)
        except C.NULLError:
            return None

    @property
    def prev_sibling(self):
        try:
            return Obj(self._obj.prev_sibling)
        except C.NULLError:
            return None

    @property
    def arity(self):
        return self._obj.arity

    @property
    def children(self):
        return [Obj(c) for c in self._obj.children]

    @property
    def first_child(self):
        try:
            return Obj(self._obj.first_child)
        except C.NULLError:
            return None

    @property
    def last_child(self):
        try:
            return Obj(self._obj.last_child)
        except C.NULLError:
            return None

    def get_userdata(self):
        return self._obj.userdata

    def set_userdata(self, data):
        try:
            self._obj.userdata = data
        except TypeError:
            raise ArgError('userdata must be integer type')

    userdata = property(get_userdata, set_userdata,
                        doc='userdata can only be an integer value')

    @property
    def cpuset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.cpuset))
        except C.NULLError:
            return None

    @property
    def complete_cpuset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.complete_cpuset))
        except C.NULLError:
            return None

    @property
    def online_cpuset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.online_cpuset))
        except C.NULLError:
            return None

    @property
    def allowed_cpuset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.allowed_cpuset))
        except C.NULLError:
            return None

    @property
    def nodeset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.nodeset))
        except C.NULLError:
            return None

    @property
    def complete_nodeset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.complete_nodeset))
        except C.NULLError:
            return None

    @property
    def allowed_nodeset(self):
        try:
            return Bitmap(C.bitmap_dup(self._obj.allowed_nodeset))
        except C.NULLError:
            return None

    @property
    def distances(self):
        return tuple([Distances(d) for d in self._obj.distances])

    @property
    def distances_count(self):
        return self._obj.distances_count

    @property
    def infos(self):
        return tuple([ObjInfo(i) for i in self._obj.infos])

    @property
    def infos_count(self):
        return self._obj.infos_count

    @property
    def symmetric_subtree(self):
        return self._obj.symmetric_subtree

    # Object/String Conversion
    @property
    def type_string(self):
        return C.obj_type_string(self.type)

    # deprecated
    @classmethod
    def type_of_string(cls, string):
        """Return an object type from the string"""
        return Obj.type_sscanf(string)[0]

    @classmethod
    def type_sscanf(cls, string):
        """Returns (int obj_type, int depth or None, int cache_type or None)"""
        return C.obj_type_sscanf(string)

    @classmethod
    def string_of_type(cls, myType):
        """return a string describing an object type"""
        return C.obj_type_string(myType)

    def type_asprintf(self, verbose=0):
        return C.obj_type_asprintf(self._obj, verbose)

    def attr_asprintf(self, separator='#', verbose=0):
        return C.obj_attr_asprintf(self._obj, separator, verbose)

    @classmethod
    def cpuset_asprintf(cls, objs):
        """Stringify the cpuset containing a set of objects"""
        l = []
        for o in objs:
            l.append(o._obj)
        return C.obj_cpuset_asprintf(l)

    def get_info_by_name(self, name):
        return C.obj_get_info_by_name(self._obj, name)

    def add_info(self, name, value):
        return C.obj_add_info(self._obj, name, value)

    def __eq__(self, other):
        """Two objects are equal if they are physically the same structure"""
        return self._obj == other._obj

    def __ne__(self, other):
        return self._obj != other._obj

    def __str__(self):
        s = ''
        for i in self.infos:
            s += ' ' + str(i)
        return self.type_asprintf() + ',' + self.attr_asprintf() + s

    # Basic Traversal Helpers
    def get_ancestor_obj_by_depth(self, depth):
        try:
            return Obj(C.get_ancestor_obj_by_depth(None, depth, self._obj))
        except C.NULLError:
            return None

    def get_ancestor_obj_by_type(self, type1):
        try:
            return Obj(C.get_ancestor_obj_by_type(None, type1, self._obj))
        except C.NULLError:
            return None

    def get_next_child(self, prev):
        if prev is not None:
            prev = prev._obj
        return Obj(C.get_next_child(None, self._obj, prev))

    def get_common_ancestor_obj(self, obj2):
        return Obj(C.get_common_ancestor_obj(None, self._obj, obj2._obj))

    @classmethod
    def get_common_ancestor(cls, obj1, obj2):
        """Returns the common parent object og 2 objects"""
        return Obj(C.get_common_ancestor_obj(None, obj1._obj, obj2._obj))

    def is_in_subtree(self, subtree_root):
        """Returns true if obj is inside the subtree"""
        return C.obj_is_in_subtree(None, self._obj, subtree_root._obj)

    # Cache-specific Finding Helpers
    def get_shared_cache_covering(self):
        """Get the first cache shared between an object and somebody else"""
        try:
            return Obj(C.get_shared_cache_covering_obj(None, self._obj))
        except C.NULLError:
            return None

    # OpenGL display specific functions
    def gl_get_display(self):
        """Get the OpenGL display port and device corresponding to this OS object"""
        try:
            return C.gl_get_display_by_osdev(None, self._obj)
        except C.NULLError:
            return None, None

    # Advanced I/O object traversal helpers
    @property
    def non_io_ancestor(self):
        """Get the first non-I/O ancestor object"""
        try:
            return Obj(C.get_non_io_ancestor_obj(None, self._obj))
        except C.NULLError:
            return None


def _typeFromString(type1):
    if type(type1) is int:
        return type1
    try:
        type1 = int(type1, 10)
        return type1
    except ValueError:
        pass
    except TypeError:
        pass
    try:
        type1 = Obj.type_of_string(type1)
    except C.ArgError:
        raise ArgError('unrecognized Type string: ' + type1)
    return type1


class TopologyDiffGeneric(object):

    def __init__(self, ptr):
        self._generic = ptr

    @property
    def type(self):
        return self._generic.type

    @property
    def next(self):
        if self._generic.next is None:
            return None
        return TopologyDiff(self._generic.next)


class TopologyDiffObjAttrUint64(object):

    def __init__(self, ptr):
        self._uint64 = ptr

    @property
    def type(self):
        return self._uint64.type

    @property
    def index(self):
        return self._uint64.index

    @property
    def oldvalue(self):
        return self._uint64.oldvalue

    @property
    def newvalue(self):
        return self._uint64.newvalue


class TopologyDiffObjAttrString(object):

    def __init__(self, ptr):
        self._string = ptr

    @property
    def type(self):
        return self._uint64.type

    @property
    def name(self):
        return self._string.name

    @property
    def oldvalue(self):
        return self._string.oldvalue

    @property
    def newvalue(self):
        return self._string.newvalue


class TopologyDiffObjAttrGeneric(object):

    def __init__(self, ptr):
        self._generic = ptr

    @property
    def type(self):
        return self._generic.type


class TopologyDiffObjAttr(object):

    def __init__(self, ptr):
        self._obj_attr = ptr

    @property
    def type(self):
        return self._obj_attr.type

    @property
    def next(self):
        if self._obj_attr.next is None:
            return None
        return TopologyDiff(self._obj_attr.next)

    @property
    def obj_depth(self):
        return self._obj_attr.obj_depth

    @property
    def obj_index(self):
        return self._obj_attr.obj_index

    @property
    def diff(self):
        return TopologyDiffObjAttrU(self._obj_attr.diff)


class TopologyDiffObjAttrU(object):

    def __init__(self, ptr):
        self._obj_attr_u = ptr

    @property
    def generic(self):
        return TopologyDiffObjAttrGeneric(self._obj_attr_u.generic)

    @property
    def uint64(self):
        assert self.generic.type in (TOPOLOGY_DIFF_OBJ_ATTR_SIZE,)
        return TopologyDiffObjAttrUint64(self._obj_attr_u.uint64)

    @property
    def string(self):
        assert self.generic.type in (
            TOPOLOGY_DIFF_OBJ_ATTR_NAME, TOPOLOGY_DIFF_OBJ_ATTR_INFO)
        return TopologyDiffObjAttrString(self._obj_attr_u.string)


class TopologyDiffTooComplex(object):

    def __init__(self, ptr):
        self._too_complex = ptr

    @property
    def type(self):
        return self._too_complex.type

    @property
    def next(self):
        if self._too_complex.next is None:
            return None
        return TopologyDiff(self._too_complex.next)

    @property
    def obj_depth(self):
        return self._too_complex.obj_depth

    @property
    def obj_index(self):
        return self._too_complex.obj_index


class TopologyDiff(object):

    def __init__(self, ptr):
        self._diff = ptr

    @property
    def generic(self):
        return TopologyDiffGeneric(self._diff.generic)

    @property
    def obj_attr(self):
        assert self.generic.type == TOPOLOGY_DIFF_OBJ_ATTR
        return TopologyDiffObjAttr(self._diff.obj_attr)

    @property
    def too_complex(self):
        assert self.generic.type == TOPOLOGY_DIFF_TOO_COMPLEX
        return self._diff.too_complex


class Topology(object):
    """ NOTE you need to hold the topology reference as long as you continue to
    hold a reference to any constituent part of it (object, difference, etc.)"""

    def __init__(self, ptr=None):
        self.userdata = None
        if ptr is None:
            self._topology = C.topology_ptr()
        else:
            self._topology = ptr

    def load(self):
        C.topology_load(self._topology)

    def check(self):
        C.topology_check(self._topology)

    # Configure Topology Detection
    def ignore_type(self, type1):
        C.topology_ignore_type(self._topology, _typeFromString(type1))

    def ignore_type_keep_structure(self, type1):
        C.topology_ignore_type_keep_structure(self._topology,
                                              _typeFromString(type1))

    def ignore_all_keep_structure(self):
        C.topology_ignore_all_keep_structure(self._topology)

    def set_flags(self, flags):
        C.topology_set_flags(self._topology, flags)

    def set_pid(self, pid):
        C.topology_set_pid(self._topology, pid)

    def set_fsroot(self, path):
        C.topology_set_fsroot(self._topology, path)

    def set_synthetic(self, string):
        C.topology_set_synthetic(self._topology, string)

    def set_xml(self, xmlpath):
        C.topology_set_xml(self._topology, xmlpath)

    def set_xmlbuffer(self, xmlbuffer):
        C.topology_set_xmlbuffer(self._topology, xmlbuffer)

    def set_custom(self):
        C.topology_set_custom(self._topology)

    def set_distance_matrix(self, obj_type, os_index, distances):
        if os_index is None:
            os_index = ()
        if distances is None:
            distances = ()
        C.topology_set_distance_matrix(
            self._topology, obj_type, os_index, distances)

    @property
    def support(self):
        return TopologySupport(C.topology_get_support(self._topology))

    # Exporting Topologies to XML
    def export_xml(self, path):
        C.topology_export_xml(self._topology, path)

    def export_xmlbuffer(self):
        return C.topology_export_xmlbuffer(self._topology)

    def set_userdata_export_callback(self, cb):
        C.topology_set_userdata_export_callback(self._topology, cb)

    def export_obj_userdata(self, reserved, obj, name, buffer1):
        """Export some object userdata to XML"""
        C.export_obj_userdata(reserved, self._topology,
                              obj._obj, name, buffer1)

    def export_obj_userdata_base64(self, reserved, obj, name, buffer1):
        """Encode and export some object userdata to XML"""
        C.export_obj_userdata_base64(reserved, self._topology, obj._obj, name,
                                     buffer1)

    def set_userdata_import_callback(self, cb):
        """Set the application-specific callback for importing userdata"""
        C.topology_set_userdata_import_callback(self._topology, cb)

    # Exporting Topologies to Synthetic
    def export_synthetic(self, flags):
        """Export the topology as a synthetic string"""
        return C.topology_export_synthetic(self._topology, flags)

    # Get Some topology Information
    @property
    def depth(self):
        return C.topology_get_depth(self._topology)

    def get_type_depth(self, type1):
        if isinstance(type1, str):
            type1 = _typeFromString(type1)
        return C.get_type_depth(self._topology, type1)

    def get_depth_type(self, depth):
        """Returns the type of objects at depth"""
        return C.get_depth_type(self._topology, depth)

    def get_nbobjs_by_depth(self, depth):
        return C.get_nbobjs_by_depth(self._topology, depth)

    def get_nbobjs_by_type(self, type1):
        return C.get_nbobjs_by_type(self._topology, type1)

    @property
    def is_thissystem(self):
        return bool(C.topology_is_thissystem(self._topology))

    def get_flags(self):
        return C.topology_get_flags(self._topology)

    # CPU binding
    def set_cpubind(self, set1, flags):
        """Bind current process or thread on cpus given in physical bitmap"""
        C.set_cpubind(self._topology, set1._bitmap, flags)

    def get_cpubind(self, flags):
        """Get current process or thread binding"""
        return Bitmap(C.get_cpubind(self._topology, flags))

    def set_proc_cpubind(self, pid, set1, flags):
        """Bind a process on cpus given in physical bitmap"""
        C.set_proc_cpubind(self._topology, pid, set1._bitmap, flags)

    def get_proc_cpubind(self, pid, flags):
        """Get the current physical binding of process"""
        return Bitmap(C.get_proc_cpubind(self._topology, pid, flags))

    def set_thread_cpubind(self, thread, set1, flags):
        """Bind a thread on cpus given in physical bitmap"""
        C.set_thread_cpubind(self._topology, thread, set1._bitmap, flags)

    def get_thread_cpubind(self, thread, flags):
        """Get the current physical binding of thread"""
        return Bitmap(C.get_thread_cpubind(self._topology, thread, flags))

    def get_last_cpu_location(self, flags):
        """Get the last physical CPU where the current process or thread ran"""
        return Bitmap(C.get_last_cpu_location(self._topology, flags))

    def get_proc_last_cpu_location(self, pid, flags):
        """Get the last physical CPU where a process ran"""
        return Bitmap(C.get_proc_last_cpu_location(self._topology, pid, flags))

    # Memory binding
    def set_membind_nodeset(self, nodeset, policy, flags):
        """Set the default memory binding policy of the current process or thread to prefer the NUMA node(s) specified by physical nodeset"""
        C.set_membind_nodeset(self._topology, nodeset._bitmap, policy, flags)

    def set_membind(self, set_, policy, flags):
        """Set the default memory binding policy of the current process or thread to prefer the NUMA node(s) near the specified physical cpuset or nodeset"""
        C.set_membind(self._topology, set_._bitmap, policy, flags)

    def get_membind_nodeset(self, flags):
        """Query the default memory binding policy and physical locality of the current process or thread
        Returns: (Bitmap, policy)"""
        b, p = C.get_membind_nodeset(self._topology, flags)
        return Bitmap(b), p

    def get_membind(self, flags):
        """Query the default memory binding policy and physical locality of the current process or thread (the locality is returned in cpuset as CPUs near the locality's actual NUMA node(s))
        Returns: (Bitmap, policy)"""
        b, p = C.get_membind(self._topology, flags)
        return Bitmap(b), p

    def set_proc_membind_nodeset(self, pid, nodeset, policy, flags):
        """Set the default memory binding policy of the specified process to prefer the NUMA node(s) specified by physical nodeset"""
        C.set_proc_membind_nodeset(self._topology, pid, nodeset._bitmap, policy,
                                   flags)

    def set_proc_membind(self, pid, set_, policy, flags):
        """Set the default memory binding policy of the specified process to prefer the NUMA node(s) near the specified physical cpuset or nodeset"""
        C.set_proc_membind(self._topology, pid, set_._bitmap, policy, flags)

    def get_proc_membind_nodeset(self, pid, flags):
        """Query the default memory binding policy and physical locality of the specified process"""
        b, p = C.get_proc_membind_nodeset(self._topology, pid, flags)
        return Bitmap(b), p

    def get_proc_membind(self, pid, flags):
        """Query the default memory binding policy and physical locality of the specified process (the locality is returned in cpuset as CPUs near the locality's actual NUMA node(s))
        Returns: (Bitmap, policy)"""
        b, p = C.get_proc_membind(self._topology, pid, flags)
        return Bitmap(b), p

    def set_area_membind_nodeset(self, addr, len1, nodeset, policy, flags):
        """Bind the already-allocated memory identified by (addr, len1) to the NUMA node(s) in physical nodeset"""
        C.set_area_membind_nodeset(self._topology, addr, len1, nodeset._bitmap,
                                   policy, flags)

    def set_area_membind(self, addr, len1, cpuset, policy, flags):
        """Bind the already-allocated memory identified by (addr, len1) to the NUMA node(s) near physical cpuset or nodeset"""
        C.set_area_membind(self._topology, addr, len1,
                           cpuset._bitmap, policy, flags)

    def get_area_membind_nodeset(self, addr, len1, flags):
        """Query the physical NUMA node(s) and binding policy of the memory identified by (addr, len1)
        Returns: (Bitmap, policy)"""
        b, p = C.get_area_membind_nodeset(self._topology, addr, len1, flags)
        return Bitmap(b), p

    def get_area_membind(self, addr, len1, flags):
        """Query the CPUs near the physical NUMA node(s) and binding policy of the memory identified by (addr, len1)
        Returns: (Bitmap, policy)"""
        b, p = C.get_area_membind(self._topology, addr, len1, flags)
        return Bitmap(b), p

    def get_area_memlocation(self, addr, len_, flags):
        """Get the NUMA nodes where memory identified by ( addr, len ) is physically allocated."""
        return Bitmap(C.get_area_memlocation(self._topology, addr, len_, flags))

    def alloc(self, len1):
        """Allocate some memory"""
        return C.alloc(self._topology, len1)

    def alloc_membind_nodeset(self, len1, nodeset, policy, flags):
        """Allocate some memory on the given physical nodeset"""
        return C.alloc_membind_nodeset(self._topology, len1, nodeset._bitmap,
                                       policy, flags)

    def alloc_membind(self, len1, cpuset, policy, flags):
        """Allocate some memory on memory nodes near the given physical cpuset or nodeset"""
        return C.alloc_membind(self._topology, len1, cpuset._bitmap, policy, flags)

    def free(self, addr, len1):
        """Free memory that was previously allocated by hwloc_alloc() or hwloc_alloc_membind*()"""
        C.free(self._topology, addr, len1)

    # Modifying a loaded topology
    def insert_misc_object_by_cpuset(self, cpuset, name):
        """Add a MISC object to the topology"""
        return Obj(C.topology_insert_misc_object_by_cpuset(self._topology,
                                                           cpuset._bitmap,
                                                           name))

    def insert_misc_object_by_parent(self, parent, name):
        """Add a MISC object as a leaf of the topology"""
        return Obj(C.topology_insert_misc_object_by_parent(self._topology,
                                                           parent._obj,
                                                           name))

    def restrict(self, cpuset, flags=0):
        """Restrict the topology to the given CPU set"""
        C.topology_restrict(self._topology, cpuset._bitmap, flags)

    def dup(self):
        """Duplicate a topology"""
        return Topology(C.topology_dup(self._topology))

    # Building Custom Topologies
    def custom_insert_topology(self, newparent, oldtopology, oldroot=None):
        """Insert an existing topology inside this custom topology"""
        if oldroot is not None:
            oldroot = oldroot._obj
        C.custom_insert_topology(self._topology, newparent._obj,
                                 oldtopology._topology, oldroot)

    def custom_insert_group_object_by_parent(self, parent, groupdepth):
        """Insert a new group object inside a custom topology"""
        return Obj(C.custom_insert_group_object_by_parent(self._topology,
                                                          parent._obj,
                                                          groupdepth))

    # Object Type Helpers
    def get_type_or_below_depth(self, type1):
        """Returns the depth of objects of type type1 or below"""
        return C.get_type_or_below_depth(self._topology, type1)

    def get_type_or_above_depth(self, type1):
        """Returns the depth of objects of type type1 or above"""
        return C.get_type_or_above_depth(self._topology, type1)

    # Retrieve Objects
    def get_obj_by_depth(self, depth, index):
        return Obj(C.get_obj_by_depth(self._topology, depth, index))

    def get_obj_by_type(self, type1, index):
        return Obj(C.get_obj_by_type(self._topology, type1, index))

    # Object/String Conversion
    def obj_asprintf(self, obj, prefix, verbose=0):
        return C.obj_asprintf(self._topology, obj._obj, prefix, verbose)

    # Basic Traversal Helpers
    @property
    def root_obj(self):
        return Obj(C.get_root_obj(self._topology))

    def get_next_obj_by_depth(self, depth, prev=None):
        """Returns the next object at depth"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_obj_by_depth(self._topology, depth, prev))
        except C.NULLError:
            return None

    def objs_by_depth(self, depth, prev=None):
        prev = self.get_next_obj_by_depth(depth, prev)
        while prev:
            yield prev
            prev = self.get_next_obj_by_depth(depth, prev)

    def get_next_obj_by_type(self, type1, prev=None):
        """ Returns the next object of type"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_obj_by_type(self._topology, type1, prev))
        except C.NULLError:
            return None

    def objs_by_type(self, type1, prev=None):
        prev = self.get_next_obj_by_type(type1, prev)
        while prev:
            yield prev
            prev = self.get_next_obj_by_type(type1, prev)

    def obj_is_in_subtree(self, obj, subtree_root):
        return bool(C.obj_is_in_subtree(self._topology, obj._obj, subtree_root._obj))

    # Finding Objects Inside a CPU set
    def get_first_largest_obj_inside_cpuset(self, set1):
        """Get the first largest object included in the given cpuset"""
        try:
            return Obj(C.get_first_largest_obj_inside_cpuset(self._topology,
                                                             set1._bitmap))
        except C.NULLError:
            return None

    def get_largest_objs_inside_cpuset(self, set1, max1):
        """Get the set of largest objects covering exactly a given cpuset"""
        try:
            l = [Obj(x) for x in C.get_largest_objs_inside_cpuset(self._topology,
                                                                  set1._bitmap,
                                                                  max1)
                 ]
            return tuple(l)
        except C.ArgError:
            raise ArgError('get_largest_objs_inside_cpuset')

    def get_next_obj_inside_cpuset_by_depth(self, set1, depth, prev=None):
        """Next same-depth object covering at least CPU set"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_obj_inside_cpuset_by_depth(self._topology,
                                                             set1._bitmap, depth,
                                                             prev))
        except C.NULLError:
            return None

    def objs_inside_cpuset_by_depth(self, set1, depth, prev=None):
        """Iterate same-depth objects covering at least the cpuset"""
        prev = self.get_next_obj_inside_cpuset_by_depth(set1, depth, prev)
        while prev:
            yield prev
            prev = self.get_next_obj_inside_cpuset_by_depth(set1, depth, prev)

    def get_next_obj_inside_cpuset_by_type(self, set1, type1, prev=None):
        """Next same-type object covering at least CPU set"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_obj_inside_cpuset_by_type(self._topology,
                                                            set1._bitmap, type1,
                                                            prev))
        except C.NULLError:
            return None

    def objs_inside_cpuset_by_type(self, set1, type1, prev=None):
        """Iterate through same-type objects covering at least the cpuset"""
        prev = self.get_next_obj_inside_cpuset_by_type(set1, type1, prev)
        while prev:
            yield prev
            prev = self.get_next_obj_inside_cpuset_by_type(set1, type1, prev)

    def get_obj_inside_cpuset_by_depth(self, set1, depth, idx):
        """ Return the index-th object at depth included in CPU set"""
        try:
            return Obj(C.get_obj_inside_cpuset_by_depth(self._topology,
                                                        set1._bitmap, depth, idx))
        except C.NULLError:
            return None

    def get_obj_inside_cpuset_by_type(self, set1, type1, idx):
        """Return the idx-th object of type included in CPU set"""
        try:
            return Obj(C.get_obj_inside_cpuset_by_type(self._topology, set1._bitmap,
                                                       type1, idx))
        except C.NULLError:
            return None

    def get_nbobjs_inside_cpuset_by_depth(self, set1, depth):
        return C.get_nbobjs_inside_cpuset_by_depth(self._topology, set1._bitmap,
                                                   depth)

    def get_nbobjs_inside_cpuset_by_type(self, set1, type1):
        return C.get_nbobjs_inside_cpuset_by_type(self._topology, set1._bitmap,
                                                  type1)

    def get_obj_index_inside_cpuset(self, set1, obj):
        """Return the logical index among the objects included in CPU set"""
        return C.get_obj_index_inside_cpuset(self._topology, set1._bitmap, obj._obj)

    # Finding a single Object covering at least a CPU set
    def get_child_covering_cpuset(self, set1, parent):
        """Get the child covering at least the CPU set"""
        try:
            return Obj(C.get_child_covering_cpuset(self._topology, set1._bitmap,
                                                   parent._obj))
        except C.NULLError:
            return None

    def get_obj_covering_cpuset(self, set1):
        """Get the lowest object covering at least the CPU set"""
        try:
            return Obj(C.get_obj_covering_cpuset(self._topology, set1._bitmap))
        except C.NULLError:
            return None

    # Finding a set of similar Objects covering at least a CPU set
    def get_next_obj_covering_cpuset_by_depth(self, set1, depth, prev=None):
        """Next same-depth object covering at least this CPU set"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_obj_covering_cpuset_by_depth(self._topology,
                                                               set1._bitmap, depth,
                                                               prev))
        except C.NULLError:
            return None

    def objs_covering_cpuset_by_depth(self, set1, depth, prev=None):
        """Iterate through same-depth objects covering at least this CPU set"""
        prev = self.get_next_obj_covering_cpuset_by_depth(set1, depth, prev)
        while prev:
            yield prev
            prev = self.get_next_obj_covering_cpuset_by_depth(
                set1, depth, prev)

    def get_next_obj_covering_cpuset_by_type(self, set1, type1, prev=None):
        """Next same-type object covering at least this CPU set"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(
                C.get_next_obj_covering_cpuset_by_type(self._topology,
                                                       set1._bitmap,
                                                       _typeFromString(type1),
                                                       prev))
        except C.NULLError:
            return None

    def objs_covering_cpuset_by_type(self, set1, type1, prev=None):
        """Iterate through same-type objects covering at least this CPU set"""
        prev = self.get_next_obj_covering_cpuset_by_type(
            set1, type1, prev)
        while prev:
            yield prev
            prev = self.get_next_obj_covering_cpuset_by_type(set1, type1, prev)

    # Cache-specific Finding Helpers
    def get_cache_type_depth(self, cachelevel, cachetype):
        """Find the depth of cache objects matching cache depth and type"""
        return C.get_cache_type_depth(self._topology, cachelevel, cachetype)

    def get_cache_covering_cpuset(self, set1):
        """Get the first cache covering a cpuset"""
        try:
            return Obj(C.get_cache_covering_cpuset(self._topology, set1._bitmap))
        except C.NULLError:
            return None

    def get_shared_cache_covering_obj(self, obj):
        """Get the first cache shared between an object and somebody else"""
        try:
            return Obj(C.get_shared_cache_covering_obj(self._topology, obj._obj))
        except C.NULLError:
            return None

    # Finding objects, miscellaneous helpers
    def get_pu_obj_by_os_index(self, os_index):
        """Returns the object of type HWLOC_OBJ_PU with os_index"""
        return Obj(C.get_pu_obj_by_os_index(self._topology, os_index))

    def get_numanode_obj_by_os_index(self, os_index):
        """Returns the object of type HWLOC_OBJ_NODE with os_index"""
        return Obj(C.get_numanode_obj_by_os_index(self._topology, os_index))

    def get_closest_objs(self, src, max1):
        """Do a depth-first traversal of the topology to find and sort
           all objects that are at the same depth as src"""
        l = C.get_closest_objs(self._topology, src._obj, max1)
        return tuple([Obj(x) for x in l])

    def get_obj_below_by_type(self, type1, idx1, type2, idx2):
        """ Find an object below another object, both specified by types and indexes"""
        try:
            return Obj(C.get_obj_below_by_type(self._topology, type1, idx1, type2,
                                               idx2))
        except C.NULLError:
            return None

    def get_obj_below_array_by_type(self, *pairs):
        """Find an object below a chain of objects specified by a list of type and index pairs"""
        typev = [x[0] for x in pairs]
        idxv = [x[1] for x in pairs]
        try:
            return Obj(C.get_obj_below_array_by_type(self._topology, typev, idxv))
        except C.NULLError:
            return None

    # Distributing items over a topology
    def distrib(self, roots, n, until, flags=0):
        """Distribute n items over the topology under roots"""
        l = tuple([x._obj for x in roots])
        l = C.distrib(self._topology, l, n, until, flags)
        return tuple([Bitmap(x) for x in l])

    # deprecated
    def distribute(self, root, n, until):
        """Distribute n items over the topology under root"""
        l = C.distribute(self._topology, root._obj, n, until)
        return tuple([Bitmap(x) for x in l])

    # deprecated
    def distributev(self, roots, n, until):
        """Distribute n items over the topology under roots"""
        l = tuple([x._obj for x in roots])
        l = C.distributev(self._topology, l, n, until)
        return tuple([Bitmap(x) for x in l])

    def alloc_membind_policy_nodeset(self, len1, nodeset, policy, flags):
        """Allocate some memory on the given nodeset
        Caller must free"""
        return C.alloc_membind_policy_nodeset(self._topology, len1, nodeset._bitmap,
                                              policy, flags)

    def alloc_membind_policy(self, len1, set_, policy, flags):
        """Allocate some memory on the memory nodes near given cpuset or nodeset
        Caller must free"""
        return C.alloc_membind_policy(self._topology, len1, set_._bitmap, policy,
                                      flags)

    # Cpuset Helpers
    @property
    def complete_cpuset(self):
        try:
            return Bitmap(C.topology_get_complete_cpuset(self._topology))
        except C.NULLError:
            return None

    @property
    def cpuset(self):
        try:
            return Bitmap(C.topology_get_topology_cpuset(self._topology))
        except C.NULLError:
            return None

    @property
    def online_cpuset(self):
        try:
            return Bitmap(C.topology_get_online_cpuset(self._topology))
        except C.NULLError:
            return None

    @property
    def allowed_cpuset(self):
        try:
            return Bitmap(C.topology_get_allowed_cpuset(self._topology))
        except C.NULLError:
            return None

    # Nodeset Helpers
    @property
    def complete_nodeset(self):
        try:
            return Bitmap(C.topology_get_complete_nodeset(self._topology))
        except C.NULLError:
            return None

    @property
    def nodeset(self):
        try:
            return Bitmap(C.topology_get_topology_nodeset(self._topology))
        except C.NULLError:
            return None

    @property
    def allowed_nodeset(self):
        try:
            return Bitmap(C.topology_get_allowed_nodeset(self._topology))
        except C.NULLError:
            return None

    # Converting between CPU sets and node sets
    def cpuset_to_nodeset(self, cpuset):
        """Convert a CPU set into a NUMA node set and handle non-NUMA cases"""
        return Bitmap(C.cpuset_to_nodeset(self._topology, cpuset._bitmap))

    def cpuset_to_nodeset_strict(self, cpuset):
        """Convert a CPU set into a NUMA node set without handling non-NUMA cases"""
        return Bitmap(C.cpuset_to_nodeset_strict(self._topology, cpuset._bitmap))

    def cpuset_from_nodeset(self, nodeset):
        """Convert a NUMA node set into a CPU set and handle non-NUMA cases"""
        return Bitmap(C.cpuset_from_nodeset(self._topology, nodeset._bitmap))

    def cpuset_from_nodeset_strict(self, nodeset):
        """Convert a NUMA node set into a CPU set without handling non-NUMA cases"""
        return Bitmap(C.cpuset_from_nodeset_strict(self._topology, nodeset._bitmap))

    # Manipulating Distances
    def get_whole_distance_matrix_by_depth(self, depth):
        """Get the distances between all objects at the given depth"""
        try:
            return Distances(C.get_whole_distance_matrix_by_depth(self._topology, depth))
        except C.NULLError:
            return None

    def get_whole_distance_matrix_by_type(self, type1):
        """Get the distances between all objects of a given type"""
        try:
            return Distances(C.get_whole_distance_matrix_by_type(self._topology, type1))
        except C.NULLError:
            return None

    def get_distance_matrix_covering_obj_by_depth(self, obj, depth):
        """Get distances for the given depth and covering some objects"""
        try:
            return Distances(C.get_distance_matrix_covering_obj_by_depth(self._topology,
                                                                         obj._obj,
                                                                         depth))
        except C.NULLError:
            return None

    def get_latency(self, obj1, obj2):
        """Get the latency in both directions between two objects"""
        return C.get_latency(self._topology, obj1._obj, obj2._obj)

    # Finding I/O objects
    def get_non_io_ancestor_obj(self, obj):
        """Get the first non-I/O ancestor object"""
        try:
            return Obj(C.get_non_io_ancestor_obj(self._topology, obj._obj))
        except C.NULLError:
            return None

    def get_next_pcidev(self, prev):
        """ Get the next PCI device in the system"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_pcidev(self._topology, prev))
        except C.NULLError:
            return None

    @property
    def pcidevs(self):
        prev = self.get_next_pcidev(None)
        while prev:
            yield prev
            prev = self.get_next_pcidev(prev)

    def get_pcidev_by_busid(self, domain, bus, dev, func):
        """Find the PCI device object matching the PCI bus id
        given domain, bus device and function PCI bus id"""
        try:
            return Obj(C.get_pcidev_by_busid(self._topology, domain, bus, dev,
                                             func))
        except C.NULLError:
            return None

    def get_pcidev_by_busidstring(self, busid):
        """Find the PCI device object matching the PCI bus id
        given as a string xxxx:yy:zz.t or yy:zz.t"""
        try:
            return Obj(C.get_pcidev_by_busidstring(self._topology, busid))
        except C.NULLError:
            return None

    def get_next_osdev(self, prev):
        """ Get the next OS device in the system"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_osdev(self._topology, prev))
        except C.NULLError:
            return None

    @property
    def osdevs(self):
        prev = self.get_next_osdev(None)
        while prev:
            yield prev
            prev = self.get_next_osdev(prev)

    def get_next_bridge(self, prev):
        """Get the next bridge in the system"""
        if prev is not None:
            prev = prev._obj
        try:
            return Obj(C.get_next_bridge(self._topology, prev))
        except C.NULLError:
            return None

    @property
    def bridges(self):
        prev = self.get_next_bridge(None)
        while prev:
            yield prev
            prev = self.get_next_bridge(prev)

    def bridge_covers_pcibus(self, domain, bus):
        """Checks whether a given bridge covers a given PCI bus"""
        return bool(C.bridge_covers_pcibus(self._topology, domain, bus))

    def get_hostbridge_by_pcibus(self, domain, bus):
        """Find the hostbridge that covers the given PCI bus"""
        try:
            return Obj(C.get_hostbridge_by_pcibus(self._topology, domain, bus))
        except C.NULLError:
            return None

    # Topology differences
    def diff_build(self, newtopology, flags=0):
        """returns TopologyDiff, (boolean) is too complex"""
        diff, too = C.topology_diff_build(self._topology, newtopology._topology,
                                          flags)
        if diff is None:
            return diff, False
        return TopologyDiff(diff), bool(too)

    def diff_apply(self, diff, flags=0):
        return C.topology_diff_apply(self._topology, diff._diff, flags)

    def diff_load_xml(self, xmlpath):
        """returns TopologyDiff, refname"""
        t, r = C.topology_diff_load_xml(self._topology, xmlpath)
        return TopologyDiff(t), r

    def diff_export_xml(self, diff, refname, xmlpath):
        C.topology_diff_export_xml(self._topology, diff._diff, refname,
                                   xmlpath)

    def diff_load_xmlbuffer(self, xmlbuffer):
        """returns TopologyDiff, refname"""
        t, r = C.topology_diff_load_xmlbuffer(self._topology, xmlbuffer)
        return TopologyDiff(t), r

    def diff_export_xmlbuffer(self, diff, refname=None):
        return C.topology_diff_export_xmlbuffer(self._topology, diff._diff,
                                                refname)

    # Linux-only helpers
    def linux_set_tid_cpubind(self, tid, set1):
        C.linux_set_tid_cpubind(self._topology, tid, set1._bitmap)

    def linux_get_tid_cpubind(self, tid):
        return Bitmap(C.linux_get_tid_cpubind(self._topology, tid))

    def linux_get_tid_last_cpu_location(self, tid):
        return Bitmap(C.linux_get_tid_last_cpu_location(self._topology,
                                                        tid))

    # OpenGL display specific functions
    def gl_get_display_osdev_by_port_device(self, port, device):
        """Get the hwloc OS device object corresponding to the OpenGL display given by port and device index"""
        return Obj(C.gl_get_display_osdev_by_port_device(self._topology, port,
                                                         device))

    def gl_get_display_osdev_by_name(self, name):
        """Get the hwloc OS device object corresponding to the OpenGL display given by name"""
        return Obj(C.gl_get_display_osdev_by_name(self._topology, name))

    def gl_get_display_by_osdev(self, osdev):
        """Get the OpenGL display port and device corresponding
        to the given hwloc OS object.
        Returns (port, device)"""
        return C.gl_get_display_by_osdev(self._topology, osdev._obj)

#	# CUDA Driver API Specific Functions
#	def cuda_get_device_pci_ids(self, cudevice):
#		"""Return the domain, bus and device IDs of the CUDA device"""
#		return C.cuda_get_device_pci_ids(self._topology, cudevice)
#
#	def cuda_get_device_cpuset(self, cudevice):
#		return Bitmap(C.cuda_get_device_cpuset(self._topology, cudevice))
#
#	def cuda_get_device_pcidev(self, cudevice):
#		try:
#			o = C.cuda_get_device_pcidev(self._topology, cudevice)
#		except C.NULLError:
#			return None
#		return Obj(o)
#
#	def cuda_get_device_osdev(self, cudevice):
#		try:
#			o = C.cuda_get_device_osdev(self._topology, cudevice)
#		except C.NULLError:
#			return None
#		return Obj(o)

    # Helpers for manipulating Linux libnuma unsigned long masks
    def cpuset_to_linux_libnuma_ulongs(self, cpuset):
        """Convert hwloc CPU set into a tuple of unsigned long
        Returns: tuple of ints, maxnode"""
        return C.cpuset_to_linux_libnuma_ulongs(self._topology, cpuset._bitmap)

    def nodeset_to_linux_libnuma_ulongs(self, nodeset):
        """Convert hwloc NUMA node set into the array of unsigned long
        Returns: tuple of ints, maxnode"""
        return C.nodeset_to_linux_libnuma_ulongs(self._topology, nodeset._bitmap)

    def cpuset_from_linux_libnuma_ulongs(self, mask, maxnode=None):
        """Convert a list of unsigned long into hwloc CPU set"""
        return Bitmap(C.cpuset_from_linux_libnuma_ulongs(self._topology, mask,
                                                         maxnode))

    def nodeset_from_linux_libnuma_ulongs(self, mask, maxnode=None):
        """Convert a list of unsigned long into hwloc NUMA node set"""
        return Bitmap(C.nodeset_from_linux_libnuma_ulongs(self._topology, mask,
                                                          maxnode))

    def cpuset_to_linux_libnuma_bitmask(self, cpuset):
        """Convert hwloc CPU set into a python-libnuma Bitmask"""
        return C.cpuset_to_linux_libnuma_bitmask(self._topology, cpuset._bitmap)

    def nodeset_to_linux_libnuma_bitmask(self, nodeset):
        """Convert hwloc NUMA node set into a python-libnuma Bitmask"""
        return C.nodeset_to_linux_libnuma_bitmask(self._topology, nodeset._bitmap)

    def cpuset_from_linux_libnuma_bitmask(self, bitmask):
        """Convert python-libnuma Bitmask into hwloc CPU set"""
        return Bitmap(C.cpuset_from_linux_libnuma_bitmask(self._topology, bitmask))

    def nodeset_from_linux_libnuma_bitmask(self, bitmask):
        """Convert python-libnuma Bitmask into hwloc NUMA node set"""
        return Bitmap(C.nodeset_from_linux_libnuma_bitmask(self._topology, bitmask))

    # Intel Xeon Phi (MIC) Specific Functions
    def intel_mic_get_device_cpuset(self, idx):
        """Get the CPU set of logical processors that are physically close to MIC device whose index is idx"""
        return Bitmap(C.intel_mic_get_device_cpuset(self._topology, idx))

    def intel_mic_get_device_osdev_by_index(self, idx):
        """Get the hwloc OS device object corresponding to the MIC device for the given index"""
        try:
            return Obj(C.intel_mic_get_device_osdev_by_index(self._topology, idx))
        except C.NULLError:
            return None

    @property
    def intel_mic_device_osdevs(self):
        i = 0
        while True:
            osdev = self.intel_mic_get_device_osdev_by_index(i)
            if osdev is None:
                break
            yield osdev
            i += 1
        return

    # NVIDIA Management Library Specific Functions
#	def nvml_get_device_osdev_by_index(self, idx):
#		try:
#			return Obj(C.nvml_get_device_osdev_by_index(self._topology, idx))
#		except C.NULLError:
#			return None
#
#	@property
#	def nvml_device_osdevs(self):
#		i = 0
#		while True:
#			osdev = self.nvml_get_device_osdev_by_index(i)
#			if osdev is None:
#				break
#			yield osdev
#			i += 1
#		return


def compare_types(type1, type2):
    """Compare the depth of two object types"""
    return C.compare_types(_typeFromString(type1), _typeFromString(type2))
