from setuptools import setup

import mash_wrapper

VERSION = mash_wrapper.__version__

setup(
    name="mash_wrapper",
    version="1.0.2",
    packages=["mash_wrapper", "mash_wrapper.utils"],
    install_requires=[
        "plotly>=2.1.0",
        "tqdm>=4.19.4"
    ],
    url="https://github.com/tiagofilipe12/mash_wrapper",
    license="GPL3",
    author="Tiago F. Jesus",
    author_email="tiagojesus@medicina.ulisboa.pt",
    description="This script runs MASH given a set of reads against specified "
                "references",
    entry_points={
        "console_scripts": [
            "mash_wrapper.py = mash_wrapper.mash_wrapper:main"
        ]
    }
)
