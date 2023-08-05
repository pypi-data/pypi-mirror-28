#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test with:
    python setup.py build_ext --inplace

create wheels with wheel installed:

python setup.py bdist_wheel
python setup.py sdist --formats=gztar


"""
DESCRIPTION = ("Low-level nucleic acid sequence manipulation tools")
LONG_DESCRIPTION = """
**libnano** is a Python package
License is GPLv2
"""

DISTNAME = 'libnano'
LICENSE = 'GPLv2'
AUTHORS = "Nick Conway, Ben Pruitt"
EMAIL = "nick.conway@wyss.harvard.edu"
URL = ""
DOWNLOAD_URL = ''
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Cython',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
]

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from Cython.Build import cythonize
import numpy.distutils.misc_util
import os
import re
import sys
import ast
import shutil

pjoin = os.path.join
rpath = os.path.relpath

# Begin modified code from Flask's version getter
# BSD license
# Copyright (c) 2015 by Armin Ronacher and contributors.
# https://github.com/pallets/flask
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('libnano/__init__.py', 'rb') as initfile:
    version = str(ast.literal_eval(_version_re.search(
                                   initfile.read().decode('utf-8')).group(1)))
# end Flask derived code

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ platform info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
IS_PY_THREE = int(sys.version_info[0] > 2)

if sys.platform == 'win32':
    extra_compile_args = ['']
else:
    extra_compile_args = ['-Wno-unused-function']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ package / module paths ~~~~~~~~~~~~~~~~~~~~~~~~~ #
PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))
MODULE_PATH = pjoin(PACKAGE_PATH, 'libnano')
# unused for now
# DATASETS_PATH =     pjoin(MODULE_PATH, 'datasets')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ include dirs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
common_include = ['libnano/src', 'libnano/core/src', 'libnano/dev/src']

# Non-python files to include in the installation
libnano_files = []

# ~~~~~~~~~~~~~~~~~~~~ configure normal c api extensions ~~~~~~~~~~~~~~~~~~~~ #
normal_extensions = []

# ~~~~~~~~~~~~~~~~~~~~~~~ configure cython extensions ~~~~~~~~~~~~~~~~~~~~~~~ #
cython_extensions = []

# ~~~~~~~~~~~~~~~~~~~ add helpers pyx, pxd, and py filess ~~~~~~~~~~~~~~~~~~~ #
helpers_fp = pjoin(MODULE_PATH, 'helpers')
# copy python 2/3 specific version of c_util.pxd to use
if IS_PY_THREE:
    shutil.copyfile(pjoin(helpers_fp, 'c_util3.pxd'), pjoin(helpers_fp, 'c_util.pxd'))
else:
    shutil.copyfile(pjoin(helpers_fp, 'c_util2.pxd'), pjoin(helpers_fp, 'c_util.pxd'))
libnano_files += [rpath(pjoin(helpers_fp, f)) for f in
                  os.listdir(helpers_fp) if ('.py' in f or '.pyx' in f or '.pxd' in f)]

def addExtension(*ext_args, **ext_kwargs):
    global libnano_files
    libnano_files += ext_kwargs['sources']
    cython_extensions.append(Extension(*ext_args, **ext_kwargs))

addExtension(
    'libnano.core.seqmetric.seqrepeat',
    depends=[],
    sources=['libnano/core/src/si_seqint.c',
             'libnano/core/src/sr_seqrepeat.c',
             'libnano/core/seqmetric/seqrepeat.pyx'],
    include_dirs=common_include + [numpy.get_include()],
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqsearch.seedfinder',
    sources=['libnano/core/seqsearch/seedfinder.pyx'],
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.cymem.cymem',
    sources=['libnano/cymem/cymem.pyx'],
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqsearch.seedmatch',
    sources=['libnano/core/seqsearch/seedmatch.pyx',
             'libnano/core/src/shl_seedhashlist.c',
             'libnano/core/src/ss_seqstr.c'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqsearch.submerpool',
    sources=['libnano/core/seqsearch/submerpool.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqint',
    depends=[],
    sources=['libnano/core/seqint.pyx', 'libnano/core/src/si_seqint.c'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)
libnano_files.append('libnano/core/seqint.pxd')
libnano_files.append('libnano/datastructures/list_bisect.pxd')

addExtension(
    'libnano.core.seqstr',
    depends=[],
    sources=['libnano/core/seqstr.pyx',
             'libnano/core/src/ss_seqstr.c'],
    include_dirs=common_include + [numpy.get_include()],
    extra_compile_args=extra_compile_args
)
libnano_files.append('libnano/core/seqstr.pxd')

addExtension(
    'libnano.core.seqgraph',
    depends=[],
    sources=['libnano/core/seqgraph.pyx',
             'libnano/core/src/ss_seqstr.c'],
    include_dirs=common_include + [numpy.get_include()],
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqmetric.seqscreen',
    depends=[],
    sources=['libnano/core/src/si_seqint.c',
             'libnano/core/src/sf_seqscreen.c',
             'libnano/core/seqmetric/seqscreen.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqmetric.seqmetric',
    depends=[],
    sources=['libnano/core/src/sm_seqmetric.c',
             'libnano/core/seqmetric/seqmetric.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.core.seqsearch.restriction',
    depends=[],
    sources=['libnano/core/seqsearch/restriction.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)
# Restriction dataset(s)
res_data_fp = pjoin(MODULE_PATH, 'datasets')
libnano_files += [rpath(pjoin(root, f), MODULE_PATH) for root, _, files in
                  os.walk(res_data_fp) for f in files if '.json' in f]

addExtension(
    'libnano.datastructures.seqrecord.feature',
    depends=[],
    sources=['libnano/datastructures/seqrecord/feature.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args
)

addExtension(
    'libnano.datastructures.seqrecord.seqrecordbase',
    depends=[],
    sources=['libnano/datastructures/seqrecord/seqrecordbase.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args,
)

addExtension(
    'libnano.core.simplethermo',
    depends=[],
    sources=['libnano/core/simplethermo.pyx'],
    include_dirs=common_include,
    extra_compile_args=extra_compile_args,
)

if IS_PY_THREE:
    addExtension(
        'libnano.helpers.bytesfmt',
        depends=[],
        sources=['libnano/helpers/bytesfmt.pyx',
                 'libnano/src/_bytesfmt.c'],
        include_dirs=common_include,
        extra_compile_args=extra_compile_args,
    )

# add header files or extra c files
for path in common_include:
    libnano_files += [rpath(pjoin(path, f)) for f in
                  os.listdir(path) if ('.h' in f or '.c' in f)]

# ~~~~~~~~~~~~~~~~~~~~~ Strip `libnano/` for package data ~~~~~~~~~~~~~~~~~~~~ #
check_libnano = 'libnano/'
lcl = len(check_libnano)
for i, f in enumerate(libnano_files):
    if f.startswith(check_libnano):
        libnano_files[i] = f[lcl:]
# unique the list
libnano_files = list(set(libnano_files))
# import pprint
# pprint.pprint(libnano_files)
# sys.exit(1)

packages = ['libnano', 'libnano.core', 'libnano.fileio',
            'libnano.helpers', 'libnano.cymem', 'libnano.core.seqsearch',
            'libnano.datastructures', 'libnano.datastructures.seqrecord',
            'libnano.datasets', 'libnano.core.seqmetric']

# ~~~~~~~~~~~~~~~ inject and build dev extensions if specified ~~~~~~~~~~~~~~ #

# Commented out by NC 2018.01.05 since we are rolling towards PyPi
script_args = sys.argv[1:]
# if '--dev' in script_args:
#     normal_extensions += dev_setup.normal_extensions
#     cython_extensions += dev_setup.cython_extensions
#     libnano_files += dev_setup.libnano_files
#     script_args.remove('--dev')
#     # packages.append('libnano.dev')

# ~~~~~~~~~~~~~~~~~~~ remove old built files if specified ~~~~~~~~~~~~~~~~~~~ #
def removeBuiltFiles():
    ''' Remove any existing *.c or *.so files from a previous build process
    '''
    print('Removing previously built files...')
    avoid_dirs = ['src', '\.git', 'build', 'klib', 'scratch']
    ads = '|'.join(['(?:%s)' % d for d in avoid_dirs])
    for root, dirs, files in os.walk(MODULE_PATH):
        if not re.search(ads, root):
            for f in files:
                if f.endswith('.c') or f.endswith('.so'):
                    print('Removing %s' % pjoin(MODULE_PATH, root, f))
                    os.remove(pjoin(MODULE_PATH, root, f))

if '--rmbuilt' in script_args:
    removeBuiltFiles()
    script_args.remove('--rmbuilt')

# ~~~~~~~~~~~~~~~~~~~~~~~ cythonize cython extensions ~~~~~~~~~~~~~~~~~~~~~~~ #
cython_ext_list = cythonize(cython_extensions)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ rock and roll ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
install_requires = ['six',
                    'cython',
                    'jinja2',
                    'numpy'
                    ]

setup(
    name=DISTNAME,
    version=version,
    maintainer=AUTHORS,
    packages=packages,
    ext_modules=normal_extensions + cython_ext_list,
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
    package_data={'libnano': libnano_files},
    maintainer_email=EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    script_args=script_args,
    zip_safe=False,
    install_requires=install_requires
)
