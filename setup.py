from __future__ import absolute_import

import os
import platform
import re
from codecs import open

from pkg_resources import parse_version
from setuptools import setup, find_packages

current_platform = platform.system().lower()
extra_includes = []

__version__ = "v0.0.dev"
with open(os.path.join("dataweaver", "_version.py"), "w") as version_file:
    version_file.write("__version__ = " + "'" + __version__ + "'\n")
    version_file.close()


def clean_version(v):
    return parse_version(v).__repr__().lstrip("<Version('").rstrip("')>")


def read(*names, **kwargs):
    return open(os.path.join(os.path.dirname(__file__), *names)).read()


current_platform = platform.system().lower()
extra_includes = []
if current_platform == "windows":
    extra_includes += ["pypyodbc", "inspect"]

packages = ["dataweaver.lib", "dataweaver.engines", "dataweaver"]

includes = [
    "xlrd",
    "future",
    "argcomplete",
    "pymysql",
    "psycopg2-binary",
    "sqlite3",
] + extra_includes

excludes = [
    "pyreadline",
    "doctest",
    "pickle",
    "pdb",
    "pywin",
    "pywin.debugger",
    "pywin.debugger.dbgcon",
    "pywin.dialogs",
    "pywin.dialogs.list",
    "Tkconstants",
    "Tkinter",
    "tcl",
    "tk",
]

setup(
    name="dataweaver",
    version=clean_version(__version__),
    description="Data dataweaver",
    long_description="{a}\n{b}".format(
        a=read("README.md"),
        b=re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGES.md")),
    ),
    author="Henry Senyondo, Ethan White",
    author_email="ethan@weecology.org",
    url="https://github.com/weecology/dataweaver",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License"
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Data",
        "Topic :: Data Processing",
        "Topic :: Data integration",
        "Topic :: Database",
    ],
    packages=find_packages(
        exclude=["hooks", "docs", "tests", "scripts", "docker", ".cache"]
    ),
    entry_points={"console_scripts": ["dataweaver = dataweaver.__main__:main"]},
    install_requires=["xlrd", "future", "argcomplete"],
    # py2app flags
    app=["__main__.py"],
    data_files=[("", ["CITATION"])],
    setup_requires=[],
)

# windows doesn't have bash. No point in using bash-completion
if current_platform != "windows":
    # if platform is OS X use "~/.bash_profile"
    if current_platform == "darwin":
        bash_file = "~/.bash_profile"
    # if platform is Linux use "~/.bashrc
    elif current_platform == "linux":
        bash_file = "~/.bashrc"
    # else write and discard
    else:
        bash_file = "/dev/null"

    argcomplete_command = 'eval "$(register-python-argcomplete dataweaver)"'
    with open(os.path.expanduser(bash_file), "a+") as bashrc:
        bashrc.seek(0)
        # register dataweaver for arg-completion if not already registered
        # when a new shell is spawned
        if argcomplete_command not in bashrc.read():
            bashrc.write(argcomplete_command + "\n")
            bashrc.close()
    os.system("activate-global-python-argcomplete")
    # register for the current shell
    os.system(argcomplete_command)

try:
    from dataweaver.compile import compile
    from dataweaver.lib.repository import check_for_updates

    check_for_updates()
    compile()
except:
    pass
