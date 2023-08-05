import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme_rst = f.read()

setup(
    name='sqlfunc',
    url='https://github.com/digitalmensch/sqlfunc',
    download_url='https://pypi.python.org/pypi/sqlitent',
    description='Clever stuff with SQL in __doc__',
    long_description=readme_rst,
    keywords='sqlite, function',
    platforms='any',
    license="MIT",
    version='0.1',
    author='Tobias Ammann',
    py_modules=['sqlfunc'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Front-Ends',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
