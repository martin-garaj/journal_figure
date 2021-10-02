# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="journal_figure", # Replace with your own username
    version="0.1.0",
    author="Martin GARAJ",
    author_email="garaj.martin@gmail.com",
    description="A python library to plot figures for journal publishing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martin-garaj/journal_figure",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
