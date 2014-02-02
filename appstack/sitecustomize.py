#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""sitecustomize.py is the magic that makes the vendor directory 
work (together with .pth files like vendor/tornado.pth). Simply 
point your PYTHONPATH at the directory containing sitecustomize.py 
and vendor will be added to the path automatically. The magic 
that makes this work is the site module, see http://docs.python.org/library/site.html. 
The site module is imported when python is initialized, it 
appends site-specific paths to the module search path.
"""

import os
import site
import sys


# renew system default encoding
try:
	sys.setdefaultencoding('utf-8')
except Exception, e:
	pass


# renew system language support
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')


BASEDIR = os.path.dirname(os.path.abspath(__file__))

PREV_SYS_PATH = list(sys.path)

# Refer from:
# https://github.com/bdarnell/tornado-production-skeleton/

# site.addsitedir adds this directory to sys.path then scans for .pth files
# and adds them to the path too.
site.addsitedir(os.path.join(BASEDIR, 'vendor'))

# addsitedir adds its directories at the end, but we want our local stuff
# to take precedence over system-installed packages.
# See http://code.google.com/p/modwsgi/issues/detail?id=112
NEW_SYS_PATH = []
for item in list(sys.path):
  if item not in PREV_SYS_PATH:
    NEW_SYS_PATH.append(item)
    sys.path.remove(item)
sys.path[:0] = NEW_SYS_PATH