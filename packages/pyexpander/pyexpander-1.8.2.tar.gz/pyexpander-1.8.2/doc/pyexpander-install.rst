Installing pyexpander
=====================

Parts of pyexpander
-------------------

pyexpander consists of scripts, python modules, documentation and configuration
files. 

Requirements
------------

pyexpander requires at least `Python <https://www.python.org>`_ version 2.5 or newer.
It can also run with python 3.

pyexpander is tested on `debian <https://www.debian.org>`_ and 
`Fedora <https://getfedora.org>`_ linux distributions but should run on all
linux distributions. It probably also runs on other flavours of unix, probably
even MacOS, but this is not tested.

It may run on windows, escpecially the `Cygwin <https://www.cygwin.com>`_
environment, but this is also not tested.

Packages
--------

pyexpander is available on `pypi <https://pypi.python.org/pypi>`_, as a debian
or rpm package, as a tar.gz and zip file. The following chapters describe how 
to install pyexpander.

Install from pypi with pip
++++++++++++++++++++++++++

In order to install pyexpander with `pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`_, 
you use the command [1]_ [2]_::

  pip3 install pyexpander

.. [1] This is the example for python 3, for python 2 the command is "pip"
.. [2] Your python 3 version of pip may have a different name, e.g. "pip-3" or "pip-3.2"

You find documentation for the usage of pip at `Installing Python Modules
<https://docs.python.org/3/installing/index.html#installing-index>`_.

Install from a debian package
+++++++++++++++++++++++++++++

There are packages for debian 7 (wheezy) and debian 8 (jessie). In order to see
what debian version you use enter::

  cat /etc/debian_version

Simply download the debian package from 

* `debian 7 packages <https://sourceforge.net/projects/pyexpander/files/debian-7>`_
* `debian 8 packages <https://sourceforge.net/projects/pyexpander/files/debian-8>`_

and install with::

  dpkg -i <PACKAGENAME>

The packages may with other debian versions or debian package based
distributions like ubuntu, but this is not tested. As a last resort you may
always install from source (see `Install from source (tar.gz or zip file)`_) or
use the python package manager (pip).

Install from a rpm package
++++++++++++++++++++++++++

There are packages for fedora 21, fedora 22 and fedora 23. In order to see what
fedora version you use enter::

  cat /etc/fedora-release

Simply download the rpm package from 

* `fedora 23 packages <https://sourceforge.net/projects/pyexpander/files/fedora-23>`_
* `fedora 24 packages <https://sourceforge.net/projects/pyexpander/files/fedora-24>`_

and install with::

  rpm -ivh  <PACKAGENAME>

The packages may work with other fedora versions or rpm package based
distributions like, redhat, scientific linux or opensuse, but this was not
tested. As a last resort you may always install from source (see `Install from
source (tar.gz or zip file)`_) or use the python package manager (pip).

Install from source (tar.gz or zip file)
++++++++++++++++++++++++++++++++++++++++

You should do this only if it is impossible to use one of the methods described
above. You find further information about this method in:

  :doc:`Installing pyexpander by running setup.py <pyexpander-install-by-setup>`

