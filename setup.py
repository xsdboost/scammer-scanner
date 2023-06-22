from distutils.core import setup

from setuptools import find_packages

setup(
    name="scammer_scan",
    version="1.0.0",
    author="Steve Volcker",
    author_email="steve.volcker@gmail.com",
    packages=find_packages(),
    url="https://github.com/xsdboost/scammer_scan",
    license="LICENSE.txt",
    description="Useful towel-related stuff.",
    install_requires=[
        "discord.py==2.3.0",
        "pony==0.7.16",
        "pytz==2023.3",
    ],
)
