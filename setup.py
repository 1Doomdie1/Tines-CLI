from setuptools import setup
from tines_cli import __version__

with open("requirements.txt", "r") as f:
    req_list = f.read().split("\n")[:-1]

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name                          = "tines-cli",
    version                       = __version__,
    description                   = "CLI tool to manage Tines tenants",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/1Doomdie1/Tines-CLI",
    author                        = "Todoran Horia",
    license                       = "GPL-3.0",
    classifiers                   = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires              = req_list,
    extras_require                = {
        "dev": ["pytest", "twine"],
    },
    python_requires               = ">=3.10",
    entry_points={
        'console_scripts': [
            'tines=tines_cli.main:main'
        ]
    }
)