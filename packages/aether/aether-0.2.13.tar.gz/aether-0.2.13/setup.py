from setuptools import setup, find_packages
from pip.req import parse_requirements


long_description = \
"""
The Aether platform is a system of applications and utilities for developers to rapidly and easily build algorithms that use satellite and geospatial data. The Aether platform is accessible by REST API and python, but operates entirely in the cloud using deferred graphs. This allows developers to build and execute applications with processing abstracted away and minimal data transfer. An important consequence of this design choice is that the same algorithm code developers use during exploration can be repackaged and deployed as mobile or web applications. These applications are entirely portable, and can be published to users or other developers through a simple URL key.

In that regard, the Aether platform is an SDK for satellite analytics and framework for mobile end user applications.

The Aether platform currently supports search of three open data available Resources: the LandSat Archive (LandSat 4 through 8 satellites), the Sentinel-2 satellite, and the USDA Cropland Data Layer, a 30m per pixel map of the US categorizing the agricultural land use annually.

The platform is designed to rapidly add new data layers, making them available through the same interface. Resources can be hosted by Aether, or made accessible via owner API, and restricted to a subset of users. The usage of each Resource and its geographic usage is tracked as well.
"""

classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: GIS',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Physics',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session='hack')
requirements = [str(ir.req) for ir in install_reqs]

# python setup.py sdist upload -r pypi
setup(
    name = 'aether',
    packages = find_packages(),
    install_requires=requirements,
    version = '0.2.13',
    description = 'Welcome to the Aether Platform',
    long_description=long_description,
    author = 'David Bernat',
    author_email = 'david.bernat@gmail.com',
    url = 'https://davidbernat.github.io/aether-user/html/index.html',
    classifiers=classifiers,
    keywords = ['satellite', 'imagery', 'remote sensing', "starlight", "platform", "gis"],
)