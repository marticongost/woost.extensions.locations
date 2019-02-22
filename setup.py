#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from setuptools import setup

setup(
    name = "woost.extensions.locations",
    version = "0.0b1",
    author = "Whads/Accent SL",
    author_email = "tech@whads.com",
    maintainer = "Marti Congost",
    maintainer_email = "marti.congost@whads.com",
    url = "http://woost.info",
    description =
        """
        Woost extension to deal with locations (geographical and / or
        political areas and units).
        """,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: ZODB",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: Catalan",
        "Natural Language :: Spanish",
        "Topic :: Internet :: WWW/HTTP :: Site Management"
    ],
    install_requires = [
        "woost>=3.0b1,<3.1"
    ],
    packages = ["woost.extensions.locations"],
    include_package_data = True,
    zip_safe = False
)

