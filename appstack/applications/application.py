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

define("cookie_secret")
define("debug", default=True, type=bool, help="global debug flag for debug options")
define("port", default=8000, type=int, help="run backend server on the given port")
define("processor", default=1, type=int, help="run backend server with the processors")
define("settings")
define("static_path")
define("template_path")


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
			"cookie_secret": options.cookie_secret,
			"static_path": options.app_static_path if options.static_path else os.path.join(os.path.dirname(__file__), "assets"),
			"template_path": options.app_template_path if options.template_path else os.path.join(os.path.dirname(__file__), "views"),
			"debug": options.debug,
		}

		handlers = [
			(r'/', controllers.IndexController),
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

	# httpserver
	httpserver = tornado.httpserver.HTTPServer(Application(), xheaders=True)
	httpserver.bind(options.port, "127.0.0.1")
	httpserver.start(options.processor if options.processor else 1)

	# WARNING: this timestamp must equal to supervisord.readear.conf stopwaitsecs = 10
	# WARNING: if not or less, the server will be killed by supervisord before max_wait_seconds_before_shutdown
	if settings.debug:
		MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0
	else:
		MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 10

	# signal handler
	def sig_handler(sig, frame):
		logging.warning("Catching Signal: %s", sig)
		tornado.ioloop.IOLoop.instance().add_callback(shutdown)

	# signal handler's callback
	def shutdown():
		logging.info("Stopping HttpServer...")
		httpserver.stop() # No longer accept new http traffic

		logging.info("IOLoop Will be Terminate in %s Seconds...", 
			MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
		instance = tornado.ioloop.IOLoop.instance()

		deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

		# recursion for terminate IOLoop.instance()
		def terminate():
			now = time.time()
			if now < deadline and (instance._callbacks or instance._timeouts):
				instance.add_timeout(now + 1, terminate)
			else:
				instance.stop() # After process all _callbacks and _timeouts, break IOLoop.instance()
				logging.info('Shutdown...')
		# process recursion
		terminate()

	# signal register
	signal.signal(signal.SIGINT, sig_handler)
	signal.signal(signal.SIGTERM, sig_handler)

	# start ioloop for socket, infinite before catch signal
	tornado.ioloop.IOLoop.instance().start()
	logging.info("Exit...")



if __name__ == '__main__':
	main()