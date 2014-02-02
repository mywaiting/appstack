#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess


authors = {"mywaiting": "zhouheng@mywaiting.com"}
version = (1, 0, 0)
release = ("2013-11-10", "11:52:32", "UTC8+", "China/Maoming")


__authors__ = authors
__version__ = '.'.join(map(str, version))
__release__ = ' '.join(map(str, release))


# get git commit revision, must run in .git folder!
try:
	(stdout, _) = subprocess.Popen(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE).communicate()
	revision = stdout.strip()
except Exception:
	revision = 'GIT COMMIT REVISION HERE'

__revision__ = revision