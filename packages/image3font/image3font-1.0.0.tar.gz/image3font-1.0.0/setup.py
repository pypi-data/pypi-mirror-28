#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="image3font",
    version="1.0.0",
    packages=["image3font"],
    package_data={
        "image3font": ["*.hy"],
    },
    scripts = ["image3font/image3font.hy", "image3font/table.hy"],
    install_requires = [
        "hy>=0.10",
        "fonttools",
        "docopt",
        "toml",
    ],
#    extras_require = ["wand"],
    author="adjivas",
    author_email="adjivas@users.noreply.github.com",
    maintainer="adjivas",
    maintainer_email="adjivas@users.noreply.github.com",
    keywords=["fontforge", "fonttools"],
    description="""a image's converter to font written in Fontforge/FontTools's Hy script.""",
    long_description=open("README.md").read(),
    include_package_data=True,
    url="https://adjivas.github.io/image3font",
    platforms=["any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Lisp",
        "Topic :: Artistic Software",
        "Topic :: Utilities",
        "Topic :: Text Processing :: Fonts",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Compilers",
    ],
    license="GPL-3",
)
