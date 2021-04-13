from os import path
from setuptools import setup, find_packages
from cat9kthousandeyesctl import Metadata

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name=Metadata.name,
    author=Metadata.author,
    author_email=Metadata.email,
    description=Metadata.description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=Metadata.repo_url,
    version=Metadata.version,
    packages=find_packages(),
    py_modules=[Metadata.name],
    install_requires=requirements,
    entry_points=f"""
        [console_scripts]
        {Metadata.name}={Metadata.name}.main:cli
        """,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "License :: Other/Proprietary License",
    ],
    license=Metadata.license,
    copyright=Metadata.copyright,
    python_requires=">=3.7",
)
