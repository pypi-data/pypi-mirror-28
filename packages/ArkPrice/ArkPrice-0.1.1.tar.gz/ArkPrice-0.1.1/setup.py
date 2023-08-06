import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="ArkPrice",
    version="0.1.1",
    description="Fetch the current price of Ark",
    long_description=read("README.md"),
    author="Highjhacker",
    author_email="jolanbeer@gmail.com",
    keywords="Ark python api price markets cryptocurrency",
    license="MIT",
    packages=["ArkPrice", "tests"],
    url="https://github.com/Highjhacker/arkprice",
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3",
    zip_safe=False
)