# setup.py

from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Load the package's __version__.py module as a dictionary
VERSION = {}
with open(HERE / "mpcagency" / "version.py") as fp:
    exec(fp.read(), VERSION)

setup(
    name="mpcagency",
    version=VERSION["__version__"],
    description="A simplified SDK for interacting with MCP (Model Context Protocol) servers.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mpcagency",
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "mcp>=0.1.0",
        "aiohttp>=3.7.4",  # Required for HTTPTransport
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
            "twine",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
