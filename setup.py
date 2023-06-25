from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="scammer_scan",
    version="1.0.0",
    author="Steve Volcker",
    author_email="steve.volcker@gmail.com",
    packages=["watcher.secrets", "watcher.utils", "watcher", "watcher.domain", "watcher.orm", "watcher.datastore"],
    package_data={"watcher": ["datastore/moderators.sqlite"]},
    url="https://github.com/xsdboost/scammer_scan",
    license="LICENSE.txt",
    description="Useful towel-related stuff.",
    install_requires=requirements,
)
