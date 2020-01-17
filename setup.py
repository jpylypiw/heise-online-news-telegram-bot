import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="heise-online-news-telegram-bot",
    version="0.0.1",
    author="Jochen Pylypiw",
    author_email="jochen@pylypiw.com",
    description=("This is the inofficial heise online telegram bot."),
    license="GPL-3.0",
    keywords="heise, telegram, telegram-bot, python3",
    url="https://github.com/jpylypiw/heise-online-news-telegram-bot",
    packages=['heise_online_bot'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
