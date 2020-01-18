"""this is the setup module for heise-online-news-telegram-bot"""
from setuptools import setup


def readme():
    """include the readme as long_description"""
    with open('README.md') as handler:
        return handler.read()


setup(
    name="heise-online-news-telegram-bot",
    version="0.0.1",
    description="This is the inofficial heise online telegram bot.",
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary'
    ],
    keywords="heise telegram telegram-bot python3",
    url="https://github.com/jpylypiw/heise-online-news-telegram-bot",
    author="Jochen Pylypiw",
    author_email="jochen@pylypiw.com",
    license="GPL-3.0",
    packages=['heise_online_bot'],
    install_requires=[
        'requests',
        'python-telegram-bot',
        'xmltodict'
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest-cov',
        'pytest'
    ]
)
