# encoding: utf-8
EXTENSIONS = ['rst2pdf', 'uploads']
MARKUP = 'restructuredtext'
PRIVATE = True
TITLE = 'Yatel Wiki'
THEME = 'yatel'


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
del sys
del os

from lconfig import *
