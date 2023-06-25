from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="scammer_scan",
    version="1.0.0",
    author="Steve Volcker",
    author_email="steve.volcker@gmail.com",
    packages=["scammer_scan.secrets", "scammer_scan.utils", "scammer_scan", "scammer_scan.domain", "scammer_scan.orm", "scammer_scan.datastore"],
    package_data={"scammer_scan": ["datastore/moderators.sqlite"]},
    url="https://github.com/xsdboost/scammer_scan",
    license="LICENSE.txt",
    description="Useful towel-related stuff.",
    install_requires=requirements,
)
