from setuptools import setup

version = '0.0.8'
name = 'dual'
short_description = '`dual` is a package for dual problem.'
long_description = """\
`dual` is a package for dual problem.
::

   from dual import dual
   print(dual("min c^T x\nA x >= b\nx >= 0"))

Requirements
------------
* Python 3

Features
--------
* nothing

Setup
-----
::

   $ pip install dual

History
-------
0.0.1 (2016-3-27)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
   "Topic :: Scientific/Engineering",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    py_modules=['dual'],
    keywords=['dual',],
    author='Saito Tsutomu',
    author_email='tsutomu.saito@beproud.jp',
    url='https://pypi.python.org/pypi/dual',
    license='PSFL',
    entry_points={
            'console_scripts':[
                'dual = dual:main',
            ],
        },
)