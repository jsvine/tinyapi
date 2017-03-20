import sys, os
from setuptools import setup, find_packages
import subprocess

NAME = "tinyapi"
HERE = os.path.abspath(os.path.dirname(__file__))
version_ns = {}
with open(os.path.join(HERE, NAME, '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup(
    name=NAME,
    version=version_ns['__version__'],
    description="Python wrapper for TinyLetter's (publicly accessible, but undocumented) API.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="tinyletter api",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    url="https://github.com/jsvine/tinyapi",
    license="MIT",
    packages=find_packages(),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        "requests",
    ],
    tests_require=[ "nose" ],
    test_suite="nosetests"
)
