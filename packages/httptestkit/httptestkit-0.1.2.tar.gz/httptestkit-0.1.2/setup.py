import codecs
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import httptestkit

class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--verbose',
            './lemming', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))

tests_require = [
    'pytest',
    'mock'
]

install_requires = [
    # Any requirements your application may have. See e.g. below
    'dnspython>=1.15.0',
    'requests>=2.12.5',
    'tldextract>=2.2.0'
]

# sdist
if 'bdist_wheel' not in sys.argv:
    try:
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')

# bdist
extras_require = {}

def long_description():
    with codecs.open('README.rst', encoding='utf-8') as f:
        return f.read()

setup(
    name='httptestkit',
    version=httptestkit.__version__,
    description='Test and gather info on a web site.',
    author=httptestkit.__author__,
    author_email='no-reply@xnode.co.za',
    license=httptestkit.__license__,
    url='https://xnode.co.za/software/httptestkit',
    packages=find_packages(),
    include_package_data=True,
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'httptestkit = httptestkit.cli:main'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
