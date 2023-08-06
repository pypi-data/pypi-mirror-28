import os
from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'epyphany',
    version = '0.1.0',
    packages=['epyphany'],
    description = ('A script for facilitating network service discovery.'),
    python_requires='>=3.5.3',

    author = 'Stumblinbear',
    author_email = 'stumblinbear@gmail.com',

    license = 'GNU',
    keywords = 'network discovery discover service broadcast packet',
    url = 'https://github.com/Secret-Web/epyphany',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: System :: Networking'
    ],
)
