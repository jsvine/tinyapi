import sys
from setuptools import setup, find_packages

setup(
    name="tinyapi",
    version="0.0.0",
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
