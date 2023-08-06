import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="Pinax Team",
    author_email="developers@pinaxproject.com",
    description="An app for including boxes of admin-controllable content in templates.",
    name="pinax-boxes",
    long_description=read("README.rst"),
    version="3.0.1",
    url="http://github.com/pinax/pinax-boxes/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "boxes": []
    },
    test_suite="runtests.runtests",
    tests_require=[
    ],
    install_requires=[
        "django-appconf>=1.0.1"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
