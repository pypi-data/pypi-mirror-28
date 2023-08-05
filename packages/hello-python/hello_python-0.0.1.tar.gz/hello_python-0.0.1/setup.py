import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hello_python",
    version = "0.0.1",
    author = "Asif Raza",
    author_email = "raoasifraza1@hotmail.com",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 test.pypi.org."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "https://github.com/raoasifraza11/hello_pyton.git",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)