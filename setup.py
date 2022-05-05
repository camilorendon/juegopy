# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

setup(
    name="SpaceBattle",
    version="1.0",
    description="juego de prueba, primer version",
    author="autor",
    author_email="juancamilo.g.0512@gmail.com",
    url="url del proyecto",
    license="tipo de licencia",
    scripts=["main.py"],
    console=["main.py"],
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None,
)