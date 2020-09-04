"""setup.py: setuptools control."""

from setuptools import setup
from xc import __version__

version = __version__

description = "A CLI tool which aims to provide a convenient operation toolbox on XCode project. You can use it to:" \
    "(1) open XCode project or workspace. (2) remove project's derived data." \
    "(3) [WIP] force kill XCode process. (4) [WIP] generate Objective-C function signatures."

with open('readme.md', encoding='utf-8') as fp:
    long_description = fp.read()

install_requires = []
with open('requirements.txt', encoding='utf-8') as fp:
    for line in fp.readlines():
        line = line.strip()
        install_requires.append(line)

setup(
    name="xcode-toolbox",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zlrs",
    author_email="zhuys123@gmail.com",
    url="https://github.com/zlrs/xcode-opener",

    include_package_data=True,
    packages=["xc"],
    entry_points={
        "console_scripts": ['xc = xc.xc:xc']  # xc.xc:xc  xc module - xc.py file - xc function
    },
    install_requires=install_requires,
    license='MIT',
    platforms=['macOS']
)
