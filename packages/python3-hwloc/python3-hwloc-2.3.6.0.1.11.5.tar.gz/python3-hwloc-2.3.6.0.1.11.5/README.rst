=================================
Python 2 and 3 bindings for hwloc
=================================

***NOTE*** There is a bug in gitlab's ReStructuredText rendering. Click the "raw" button to see all of this file

I have retired and am no longer maintaining or developing this. I could work on it more if anyone is interested in using it.

If there is someone who would like to take it over, please contact me.

Example pip install from git source with virtualenv for Python2 on Fedora:

.. code:: bash
   sudo dnf install python2 python2-devel python2-tools numactl-libs \
      numactl-devel gettext pandoc texlive hwloc-devel hwloc-libs \
      libibverbs libibverbs-devel python2-libs
   virtualenv -p python2 p2hwloc
   cd p2hwloc/
   source bin/activate
   pip install Cython Babel
   pip install python2-libnuma
   pip install python2-hwloc
   # try it!
   python2 -c "import hwloc;print hwloc.version_string()"

Example for Python3 on Fedora:

.. code:: bash
   sudo dnf install python3 python3-devel python3-tools hwloc-devel \
      hwloc-libs libibverbs libibverbs-devel numactl-libs numactl-devel \
      gettext pandoc texlive python3-libs
   virtualenv -p python3 p3hwloc
   cd p3hwloc
   source bin/activate
   pip install Cython Babel
   pip install python3-libnuma
   pip install python3-hwloc
   # try it!
   python3 -c "import hwloc;print(hwloc.version_string())"

Debian9, Python2:

.. code:: bash
   sudo apt-get update
   sudo apt-get install build-essential virtualenv libpython2.7-dev \
      libnuma-dev libhwloc-dev libibverbs-dev
   virtualenv -p python2 p2pip
   cd p2pip
   source bin/activate
   pip install Cython Babel
   pip install python2-libnuma
   pip install python2-hwloc
   # try it!
   python2 -c "import hwloc;print hwloc.version_string()"

Python3 on Debian9:

.. code:: bash
   sudo apt-get update
   sudo apt-get install build-essential virtualenv libpython3.5-dev \
      libnuma-dev libhwloc-dev libibverbs-dev
   virtualenv -p python3 p3pip
   cd p3pip
   source bin/activate
   pip install Cython Babel
   pip install python2-libnuma
   pip install python2-hwloc
   # try it!
   python3 -c "import hwloc;print(hwloc.version_string())"
