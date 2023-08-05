"""GRIP Python setup module.

See:
https://github.com/crowdcomms/grip-python
"""
from setuptools import setup, find_packages
from codecs import open
import os

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(PACKAGE_DIR)

__version__ = None
with open('grip_intros/version.py') as f:
    exec(f.read())


setup(
    # Project
    name='grip-intros',
    version=str(__version__),
    description='Python client for GRIP meetings API',
    long_description=open(os.path.join(PACKAGE_DIR, 'README.md')).read(),
    url='https://github.com/crowdcomms/grip-python',

    # Author
    author='Ben Harling',
    author_email='bharling@crowdcomms.co.uk',
    license='MIT',

    # Classifiers - https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        'Development Status :: 2 - Pre-Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # License
        'License :: OSI Approved :: MIT License',
        # Python versions you support
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='grip client meetings connections things api',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,

    # Requirements - https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'requests==2.18.4',
    ],

    # List additional groups of dependencies here - pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [
            'pytest==3.0.4',
            'pytest-cov==2.4.0',
            'pytest-pep8==1.0.6',
            'responses==0.5.1'
        ],
    },
)
