This project is a proposed change to the `tuna` GUI.
See the User Guide in the 'doc' directory.

Fedora and CentOS repos at 'https://copr.fedorainfracloud.org/coprs/streeter/python-hwloc/'

Example Debian9 install:

.. code:: bash
   sudo apt-get install build-essential virtualenv python-pip libpython2.7-dev \
      libnuma-dev libhwloc-dev libibverbs-dev cython python-babel \
      git libhwloc5 python-gobject python-cairo pkg-config
   git clone https://git.kernel.org/pub/scm/libs/python/python-schedutils/python-schedutils.git/
   sudo pip install ./python-schedutils
   git clone https://git.kernel.org/pub/scm/libs/python/python-linux-procfs/python-linux-procfs.git/
   sudo pip install ./python-linux-procfs
   sudo pip install pianofish
   sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

*Note* GitLab has a bug rendering ReStructuredText files. If you cannot read the example above, click the "Open Raw" button.

*Note* `pianofish` and its dependencies must be installed system-wide. It will not work in a virtualenv or a `--user` install.

*Note* `pip uninstall pianofish` will refuse to remove some files. Look for the messages about this, and manually remove the files when uninstalling.
