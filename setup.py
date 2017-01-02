from setuptools import setup, find_packages

VERSION = '1.0.dev28'

setup(
        version=VERSION,
        packages=find_packages(exclude=["tests.*", "tests"]),
        install_requires=[
            'docutils>=0.3',
            'lxml'],
)
