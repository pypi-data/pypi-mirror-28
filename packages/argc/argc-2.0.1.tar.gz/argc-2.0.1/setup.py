from setuptools import setup
from argc.version import __version__


setup(
    name="argc",
    version=__version__,
    description="A argument parsing module for python 2 and 3",
    author="Javad Shafique",
    author_email="javadshafique@hotmail.com",
    license="MIT",
    packages=["argc"],
    include_package_data=True,
    url="https://github.com/JavadSM/argc",
    long_description=open("README.md", "r").read()
)
