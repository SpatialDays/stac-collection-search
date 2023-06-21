from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'STAC Collection Search helper utility'
LONG_DESCRIPTION = 'STAC Collection Search helper which enables a collection search on the stac-fastapi'

requirements = []
requirements_file = "./requirements.txt"
if os.path.isfile(requirements_file):
    with open(requirements_file) as f:
        requirements = f.read().splitlines()
else:
    print("requirements.txt not found")
    exit(1)

# Setting up
setup(
    name="stac_collection_search",
    version=VERSION,
    author="Ivica Matic",
    author_email="<ivica.matic@spatialdays.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python', 'azure', 'stac', 'fastapi', 'eo', 'earth observation', 'spatial', 'search', 'collection'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)