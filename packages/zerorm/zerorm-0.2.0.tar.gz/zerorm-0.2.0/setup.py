from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='zerorm',
    version='0.2.0',
    description='Looks like ORM and stores your data',
    long_description=readme,
    author='Aleksandr Mironov',
    author_email='a.m.mironov@gmail.com',
    url='https://github.com/hedin/zerorm',
    license='MIT',
    packages=find_packages(exclude=['testing', ]),
    install_requires=[
        'tinydb==3.7.0',
        'schematics==2.0.1',
        'lifter==0.4.1',
    ],
    extras_require={
        'dev': [
            'pytest==3.3.1',
            'pylint==1.8.1',
            'flake8==3.5.0',
            'isort==4.2.15',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
