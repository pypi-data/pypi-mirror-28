#!/usr/bin/python
#
# Copyright (C) 2015-2017 Red Hat, Inc.
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

from __future__ import print_function

import os
import errno

from setuptools import Command, setup
from distutils.command.build import build
from babel.messages.frontend import compile_catalog as _compile_catalog
from babel.messages.frontend import init_catalog as _init_catalog

_package_name = 'pianofish'
__author = 'Guy Streeter'
__author_email = 'guy.streeter@gmail.com'
__license = 'GPLv2+'
__description = 'pianofish process management tool'
__version = '1.0.1'
__url = 'https://gitlab.com/guystreeter/pianofish'
__classifiers = [
    'Environment :: X11 Applications :: GTK',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: System :: Systems Administration',
    ]
__install_requires = [
    'python2-hwloc',
    ]
with open('README.rst') as rfile:
    __long_description = rfile.read()


datadir = os.environ.get('DATADIR', 'share')
docdir = os.path.join(datadir, 'doc', _package_name)
licdir = os.environ.get('LICENSEDIR', docdir)
configdir = os.environ.get('CONFIGDIR', '/etc')
sysfiledir = os.environ.get('SYSFILEDIR', '/usr/share')
libexecdir = os.environ.get('LIBEXECDIR', '/usr/libexec')

po_list = []
mo_build_list = []

glibdir = os.path.join(sysfiledir, 'glib-2.0', 'schemas')
polkitdir = os.path.join(sysfiledir, 'polkit-1', 'actions')
appsdir = os.path.join(datadir, 'applications')
pkgdir = os.path.join(sysfiledir, _package_name)
dbus_datadir = os.path.join(sysfiledir, 'dbus-1', 'system-services')
dbus_configdir = os.path.join(configdir, 'dbus-1', 'system.d')

data_files = [
    (licdir, ['COPYING',
              'LICENSE',
              ]
     ),
    (docdir, ['doc/Pianofish User Guide.pdf']),
    # TODO: compile the schemas?
    (glibdir, ['src/org.fedora.pianofish.gschema.xml']),
    (polkitdir, ['src/org.fedora.pianofish1.policy']),
    (appsdir, ['src/pianofish.desktop']),
    (pkgdir, ['src/pianofish.svg']),
    (dbus_datadir, ['src/org.fedora.pianofish1.service']),
    (dbus_configdir, ['src/org.fedora.pianofish1.conf']),
    (libexecdir, ['src/pianofish/pianofish_server.py'])
]

in_dir = 'translations/locale'
if os.path.exists(in_dir):
    for lang in os.listdir(in_dir):
        src_file = os.path.join(in_dir, lang)
        if os.path.isdir(src_file):
            src_file = os.path.join(src_file,
                                    'LC_MESSAGES',
                                    _package_name+'.mo')
            install_path = os.path.join(datadir,
                                        'locale',
                                        lang,
                                        'LC_MESSAGES',)
            data_files.append((install_path, [src_file]))


class CompileMyCatalog(_compile_catalog, object):
    def initialize_options(self):
        super(CompileMyCatalog, self).initialize_options()
        self.domain = _package_name


class InitMyCatalog(_init_catalog, object):
    def initialize_options(self):
        super(InitMyCatalog, self).initialize_options()
        self.domain = _package_name


class all_build(build):
    sub_commands = [('compile_catalog', None)] + build.sub_commands

setup(name=_package_name,
      version=__version,
      description=__description,
      author=__author,
      author_email=__author_email,
      url=__url,
      license=__license,
      classifiers=__classifiers,
      install_requires=__install_requires,
      long_description=__long_description,
      package_dir={'':'src',},
      packages=['pianofish'],
      scripts=['src/bin/pianofish'],
      data_files=data_files,
      cmdclass={'build': all_build,
                'compile_catalog': CompileMyCatalog,
                'init_catalog': InitMyCatalog,
                },
      )
