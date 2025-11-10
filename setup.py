#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='nids-ipv6-config',
    version='1.0.0',
    description='NIDS IPv6 Configuration Application',
    author='DevOps Team',
    author_email='devops@example.com',
    url='https://github.com/your-org/nids-ipv6-config',
    py_modules=['nids_ipv6_config'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'nids-ipv6-config=nids_ipv6_config:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
