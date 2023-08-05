from setuptools import setup

import gpxconverter as gpx

setup(
    name=gpx.__title__,

    version=gpx.__version__,

    description=gpx.__summary__,

    license=gpx.__license__,

    url=gpx.__uri__,

    download_url=gpx.__download_url__,

    author=gpx.__author__,

    author_email=gpx.__email__,

    classifiers=[
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    packages=["gpxconverter"],

    entry_points={
        "console_scripts": [
            "gpxconverter = gpxconverter.__main__:main",
        ],
    },
)
