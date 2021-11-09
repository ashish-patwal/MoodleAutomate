from setuptools import setup, find_packages

# import io
# import re

with open("README.md", "r") as fh:
    long_description = fh.read()

# with io.open("moodle_automate/__version__.py", "rt", encoding="utf8") as fh:
#    version = re.search(r"__version__ = \"(.*?)\"", fh.read()).group(1)

setup(
    name="moodle_automate",
    version="1.0.1",
    author="Ashish Patwal",
    author_email="ashishpatwal147@gmail.com",
    description="A python program to automate Moodle Platform",
    package=find_packages(where="moodle_automate"),
    url="https://github.com/ashish-patwal/MoodleAutomate",
    install_requires=[
        "html5lib>=1.1",
        "tabulate>=0.8.9",
        "urllib3>=1.26.7",
        "inquirer>=2.7.0",
        "requests>=2.26.0",
        "soupsieve>=2.2.1",
        "beautifulsoup4>=4.10.0",
    ],
    long_description=long_description,
    python_requires=">=3.9.7",
    entry_points="""
    [console_scripts]
    moodle=moodle_automate.cli:main
    """,
)
