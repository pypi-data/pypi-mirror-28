#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import glob
import pip
if False:
    from typing import Any, Dict, Optional

import generate_manifest

ZULIP_BOTS_VERSION = "0.4.0"
IS_PYPA_PACKAGE = True

# IS_PYPA_PACKAGE is set to True by tools/release-packages
# before making a PyPA release.
if not IS_PYPA_PACKAGE:
    generate_manifest.generate_dev_manifest()

# We should be installable with either setuptools or distutils.
package_info = dict(
    name='zulip_bots',
    version=ZULIP_BOTS_VERSION,
    description='Zulip\'s Bot framework',
    author='Zulip Open Source Project',
    author_email='zulip-devel@googlegroups.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Chat',
    ],
    url='https://www.zulip.org/',
    entry_points={
        'console_scripts': [
            'zulip-run-bot=zulip_bots.run:main',
            'zulip-terminal=zulip_bots.terminal:main'
        ],
    },
    include_package_data=True,
    cmdclass={
        'gen_manifest': generate_manifest.GenerateManifest,
    },
)  # type: Dict[str, Any]

setuptools_info = dict(
    install_requires=[
        'pip',
        'zulip',
    ],
)

try:
    from setuptools import setup, find_packages
    package_info.update(setuptools_info)
    package_info['packages'] = find_packages()

except ImportError:
    from distutils.core import setup
    from distutils.version import LooseVersion
    from importlib import import_module

    # Manual dependency check
    def check_dependency_manually(module_name, version=None):
        # type: (str, Optional[str]) -> None
        try:
            module = import_module(module_name)  # type: Any
            if version is not None:
                assert(LooseVersion(module.__version__) >= LooseVersion(version))
        except (ImportError, AssertionError):
            if version is not None:
                print("{name}>={version} is not installed.".format(
                    name=module_name, version=version), file=sys.stderr)
            else:
                print("{name} is not installed.".format(name=module_name), file=sys.stderr)
            sys.exit(1)

    check_dependency_manually('zulip')
    check_dependency_manually('mock', '2.0.0')
    check_dependency_manually('html2text')
    check_dependency_manually('PyDictionary')

    # Include all submodules under bots/
    package_list = ['zulip_bots']
    dirs = os.listdir('zulip_bots/bots/')
    for dir_name in dirs:
        if os.path.isdir(os.path.join('zulip_bots/bots/', dir_name)):
            package_list.append('zulip_bots.bots.' + dir_name)
    package_info['packages'] = package_list

setup(**package_info)

# Install all requirements for all bots. get_bot_paths()
# has requirements that must be satisfied prior to calling
# it by setup().
current_dir = os.path.dirname(os.path.abspath(__file__))
bots_dir = os.path.join(current_dir, "zulip_bots", "bots")
bots_subdirs = map(lambda d: os.path.abspath(d), glob.glob(bots_dir + '/*'))
bot_paths = filter(lambda d: os.path.isdir(d), bots_subdirs)
for bot_path in bot_paths:
    req_path = os.path.join(bot_path, 'requirements.txt')
    rcode = pip.main(['install', '-r', req_path, '--quiet'])
