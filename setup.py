"""Setup file for the Forest Project in Python."""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="forest-python",
    version="0.1.2",
    description="The Forest Project in Python",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/shunsvineyard/forest-python",
    author="Shun Huang",
    author_email="zsh@shunsvineyard.info",
    license="MIT",
    keywords="tree data-structures",
    packages=setuptools.find_packages(exclude=["examples", "tests"]),
    python_requires=">=3.9",
)
