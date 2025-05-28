#!/usr/bin/env python3
"""
Setup configuration for dsa-commiter CLI tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dsa-commiter",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for managing DSA files and Git operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dsa-commiter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "rich>=12.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dsa-commiter=dsa_commiter.cli_interface:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)