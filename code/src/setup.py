#!/usr/bin/env python

import os
from distutils.core import setup

def _fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return _fullsplit(head, [tail] + result)

def get_packages(basepkg_name, root_dir=''):
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages = []
    root_dir = os.path.join(os.path.dirname(__file__), root_dir)
    cwd = os.getcwd()
    if root_dir != '':
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(basepkg_name):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'): del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(_fullsplit(dirpath)))
    
    os.chdir(cwd)
    return packages

basepkg_name = 'com'
packages = get_packages(basepkg_name)

setup(name='slipstream-mta',
      packages=packages,
      data_files=[('/etc/slipstream', ['etc/mta.cfg']),
                  ('/usr/bin', ['bin/slipstream-mta']),
                  ('/etc/init.d',['etc/slipstream-mta'])],
      requires=['com.sixsq.slipstream', 'boto', 'daemon', 'dirq'])
