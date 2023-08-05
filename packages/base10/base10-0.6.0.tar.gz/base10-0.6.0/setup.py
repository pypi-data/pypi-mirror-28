import re
from setuptools import setup, find_packages


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='base10',
    version=find_version('base10/__init__.py'),
    packages=find_packages(exclude=('test*', )),
    package_dir={'base10': 'base10'},
    url='https://github.com/mattdavis90/base10',
    license='MIT',
    author='Matt Davis',
    author_email='mattdavis90@googlemail.com',
    install_requires=('six'),
    tests_require=(),
    description=(
        'Base10 is a metrics abstractoin layer for linking multiple '
        'metrics source and stores. It also simplifies metric creation '
        'and proxying.'
    ),
    long_description=read('README.rst'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
