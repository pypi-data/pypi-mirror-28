#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
from pip.req import parse_requirements

try:
    from setuptools import setup, find_packages
    setup
except ImportError:
    from distutils.core import setup
    setup    

    
PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

install_reqs = parse_requirements(os.path.join(PACKAGE_PATH, 'requirements.txt'),
                                  session=False)
requirements = [str(ir.req) for ir in install_reqs]
    
with open(os.path.join(PACKAGE_PATH, 'README.rst')) as readme_file:
    README = readme_file.read()
    
with open(os.path.join(PACKAGE_PATH, 'pySPT/__init__.py')) as version_file:
    version_file = version_file.read()
    VERSION = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                        version_file, re.M)
VERSION = VERSION.group(1)    
    
PACKAGES = ['pySPT',
            'pySPT.catalog',
            'pySPT.decorators',
            'pySPT.grid',
            'pySPT.integrals',
            'pySPT.lensing',
            'pySPT.multiproc',
            'pySPT.sourcemapping',
            'pySPT.spt',
            'pySPT.tests',
            'pySPT.tools']

setup(name='pySPT',
      version='0.1',
      description='Package dedicated to the source position transformation in lens modeling.',
      long_description=README,
      author='Olivier Wertz',
      author_email='owertz@alumni.ulg.ac.be',
      license='MIT',
      url='https://github.com/owertz/pySPT',
      download_url = 'https://github.com/owertz/pySPT/archive/0.1.tar.gz',
      packages=PACKAGES,
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False,
      keywords='SPT',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX :: Linux',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7'
                  ]
)
