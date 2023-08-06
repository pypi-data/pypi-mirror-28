from __future__ import print_function  
from setuptools import setup, find_packages  
import sys
setup(
	name = 'nester_lzs',
	version = '1.3.0',
	py_modules = ['nester'],
	author = 'hfpython',
	author_email = 'hfpython@headfirstlabs.com',
	url = 'http://www.headfirstlabs.com',
	description = 'A simple printer of nested lists',
    classifiers=[  
        "Environment :: Web Environment",  
        "Intended Audience :: Developers",  
        "Operating System :: OS Independent",  
        "Topic :: Text Processing :: Indexing",  
        "Topic :: Utilities",  
        "Topic :: Internet",  
        "Topic :: Software Development :: Libraries :: Python Modules",  
        "Programming Language :: Python",  
        "Programming Language :: Python :: 2",  
        "Programming Language :: Python :: 2.6",  
        "Programming Language :: Python :: 2.7",  
    ], 
)