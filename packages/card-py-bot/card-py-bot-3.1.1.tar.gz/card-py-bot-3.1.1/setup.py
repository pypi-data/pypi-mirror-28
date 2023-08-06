"""card-py-bot setup"""

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="card-py-bot",
    version="3.1.1",
    description="A Discord Bot for embedding WOTC Magic card links "
                "into Discord",
    long_description=readme(),
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    url="https://github.com/nklapste/card-py-bot",
    download_url="https://github.com/nklapste/card-py-bot/archive/3.1.1.tar.gz",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["test"]),
    package_data={
        "": ["README.md"],
        "card_py_bot": ["MANA_ICONS/*.gif"],
    },
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "discord.py",
    ],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["card-py-bot = card_py_bot.__main__:main"],
    },
)
