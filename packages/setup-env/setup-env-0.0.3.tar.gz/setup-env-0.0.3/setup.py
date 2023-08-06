#! /usr/bin/env python3

from distutils.core import setup

setup(name="setup-env",
      description="Setup development evnironment tools.",
      version="0.0.3",
      author="Chenyao2333",
      author_email="louchenyao@gmail.com",
      url="https://github.com/Chenyao2333/setup-env",
      packages=["setup_env"],
      package_data={"setup_env": ["scripts/*"]},
      python_requires = ">=3"
)
