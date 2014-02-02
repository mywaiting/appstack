#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import os.path
import signal
import sys
import sys.path
import time

import tornado
import tornado.web
import tornado.locale
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options

try:
	import appstack
except ImportError:
	APPSDIR = os.path.realpath("..") # /appstack/application
	BASEDIR = os.path.join(APPSDIR, "..") # /appstack
	sys.path.append(BASEDIR) # /appstack

import appstack
import appstack.applications
import appstack.database
import appstack.libraries
import appstack.settings
import appstack.vendor

from appstack.applications import controllers, models
from appstack.database import schema, seeds
# from appstack.settings import *


# --- const vars ---

APPSDIR = os.path.realpath("..") # /appstack/application
BASEDIR = os.path.join(APPSDIR, "..") # /appstack

# --- default settings ---

define("debug", default=True, type=bool, help="global debug flag for debug options")
define("port", default=8000, type=int, help="run backend server on the given port")
define("processor", default=1, type=int, help="run backend server with the processors")
define('settings')

define('app_static_path')
define('app_template_path')


# --- global vars ---

cache = models.Redis() \
		if options.debug else models.Redis()
database = models.SQLAlchemy(options.database) \
		if options.debug else \
		models.SQLAlchemy(options.database, pool_size=10, pool_recycle=7200)


# --- application ---

class Application(tornado.web.Application):
	def __init__(self):
		settings = {
			"static_path": options.app_static_path if options.app_static_path else os.path.join(os.path.dirname(__file__), "assets"),
			"template_path": options.app_template_path if options.app_template_path else os.path.join(os.path.dirname(__file__), "views"),
			"debug": options.debug,
		}

		handlers = [
			(r'/', controllers.IndexController),
			(r'/settings', controllers.SettingsHandler),
		]

		super(Application, self).__init__(handlers, **settings)

		# --- global application vars ---

		self.cache = cache # redis
		self.database = database # postgresql


# --- main ---

def main():
	tornado.options.parse_command_line()
	# settings
	if options.settings:
		tornado.options.parse_config_file(options.settings)
	else:
		tornado.options.parse_config_file(os.path.join(BASEDIR, 'settings'))
	# i18n translations
	# tornado.locale.load_translations(settings.TRANSLATIONDIR) 
	# tornado.locale.get_supported_locales()
	# tornado.locale.set_supported_locales("en_US")



if __name__ == '__main__':
	main()