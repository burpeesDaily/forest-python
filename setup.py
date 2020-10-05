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
    version="0.0.2",
    description="The Forest Project in Python",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/shunsvineyard/forest-python",
    author="Shun Huang",
    author_email="shunsvineyard@protonmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7"
    ],
    keywords="tree data-structures",
    packages=setuptools.find_packages(exclude=["examples", "tests"]),
    entry_points={
        "console_scripts": [
            "forest-cli=pyforest.bin.forest_cli:main"
        ]
    },
    python_requires=">=3.7"
)
