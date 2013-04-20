"""\
Provides a command line tool to synchronize web site redirects with an
Amazon S3 bucket.
"""

import sys
try:
    from setuptools import setup
except ImportError:
    sys.exit("""Error: Setuptools is required for installation.
 -> http://pypi.python.org/pypi/setuptools
 or http://pypi.python.org/pypi/distribute""")

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name = "s3redirect",
    version = "0.1.2",
    description = "Synchronize web site redirects with an Amazon S3 bucket",
    author = "Nathan Grigg",
    author_email = "nathan@nathanamy.org",
    url = "http://github.com/nathangrigg/s3redirect/",
    py_modules = ["s3redirect"],
    keywords = ["Amazon", "S3", "static site", "redirect"],
    entry_points = {
        'console_scripts': ['s3redirect = s3redirect:main']
    },
    license = "BSD",
    install_requires = ['boto>=2.8.0'],
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Environment :: Console",
        ],
    long_description = __doc__,
    **extra
)
