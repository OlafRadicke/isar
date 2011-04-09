#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path

absolut_path = os.path.abspath(__file__)
absolutedir = os.path.dirname(absolut_path)
#global BASEDIR 
BASEDIR = os.path.split(absolutedir)[0]
ICONDIR = _icon_pah = os.path.join(BASEDIR + '/icons/')