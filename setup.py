"""
The setup for installation of the app.
Helpful resource:
https://docs.python.org/3.6/distutils/setupscript.html
"""

from setuptools import setup, find_packages

setup(
    name="dublin_bikes",
    version=0.1,
    description="Web app for occupancy of Dublin bike stations",
    author="Andrew Cameron, Liga Ozolina, Mereta Degutyte, Laura Boyles",
    author_email="andrew.cameron1@ucdconnect.ie",
    keywords="Dublin bikes weather",
    packages=find_packages(),
    package_dir={"src": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=open("requirements.txt", "rt").readlines(),
    entry_points={'console_scripts': ['dublin-bikes = src.app:main']}
)
