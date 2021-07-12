import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Avoid potential permissions issues with snapcraft by setting the umask
os.umask(0o022)

setuptools.setup(
    name="teamtime",
    version="9a",
    author="Joe McManus",
    author_email="josephmc@alumni.cmu.edu",
    description="teamTime is a tool to aid the problem of keeping track of "
    "time for a globally distributed team.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joemcmanus/teamTime",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=["geopy", "pandas", "plotly", "prettytable", "pytz"],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["teamtime=teamtime.teamtime:main"]},
)
