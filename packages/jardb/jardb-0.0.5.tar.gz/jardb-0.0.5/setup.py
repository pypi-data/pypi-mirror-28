import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 7):
    raise NotImplementedError("Python 2.7+ are required.")

import jardb

with open('README.rst') as fp:
    readme = fp.read()
 
with open('LICENSE') as fp:
    license = fp.read()
 
setup(name='jardb',
      version=jardb.__version__,
      description='A small Document Oriented Databse',
      long_description=readme,
      author='Lutong Chen',
      author_email='lutong98@mail.ustc.edu.cn',
      maintainer='Lutong Chen',
      maintainer_email='lutong98@mail.ustc.edu.cn',
      url='https://github.com/andytt/jardb',
      packages=['jardb'],
      license=license,
      platforms=['any'],
      classifiers=[
        'Intended Audience :: Developers',  
        'License :: OSI Approved :: MIT License',  
        'Natural Language :: English',  
        'Operating System :: OS Independent',  
        'Programming Language :: Python',    
        "Programming Language :: Python :: 2.7",     
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Utilities",
      ]
      )