from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import setuptools


setuptools.setup(
    name='gym-wrappers',
    version='0.1.0',
    description='Wrappers for common manipulations of Gym environments.',
    license='Apache 2.0',
    url='http://github.com/danijar/gym-wrappers',
    install_requires=[
        'numpy',
        'gym',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
    ],
)
