from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

packages = ["tvshowrenamer"]

about = {}
with open(os.path.join(here, "tvshowrenamer", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

with open("requirements.txt", "r", "utf-8") as f:
    requirements = f.read().strip().split("\n")

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    package_data={"": ["LICENSE"],},
    package_dir={"tvshowrenamer": "tvshowrenamer"},
    include_package_data=True,
    python_requires="!=2.7, >=3.0.*",
    install_requires=requirements,
    license=about["__license__"],
    keywords="renamer media tvshow tv automation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["tvshowrenamer = tvshowrenamer.main:main"]},
)
