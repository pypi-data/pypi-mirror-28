"""
Setup for Docs Configuration
"""
from setuptools import setup, find_packages

setup(
    name='lfdocs_conf',
    packages=['docs_conf'],
    version='0.1.1',
    author="Linux Foundation Releng",
    author_email="releng@linuxfoundation.org",
    url="https://gerrit.linuxfoundation.org/docs-conf",
    package_data={
        'docs_conf': ['defaults/*']
    },
    install_requires=[
        'sphinx',
        'sphinx_bootstrap_theme'
    ]
)
