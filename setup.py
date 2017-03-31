"""
The setup for installation of the app.
Helpful resource:
https://docs.python.org/3.6/distutils/setupscript.html
"""

from distutils.core import setup

setup(
    name="dublin_bikes",
    version=0.1,
    description="Web app for occupancy of Dublin bike stations",
    author="Andrew Cameron, Liga Ozolina, Mereta Degutyte, Laura Boyles",
    author_email="andrew.cameron1@ucdconnect.ie",
    keywords="Dublin bikes weather",
    # packages=[],
    #package_dir={"": "src"},
    install_requires=open("requirements.txt", "rt").readlines(),
    entry_points={'console_scripts': ['dublin-bikes = src.__main__:main']}
)
