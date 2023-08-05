import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme_rst = f.read()

setup(
    name='silo',
    url='https://github.com/digitalmensch/silo',
    download_url='https://pypi.python.org/pypi/silo',
    description='Simply Logging',
    long_description=readme_rst,
    keywords='logging, simple, json, audit',
    platforms='any',
    license="MIT",
    version='0.2',
    author='Tobias Ammann',
    py_modules=['silo'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Front-Ends',
    ],
)
