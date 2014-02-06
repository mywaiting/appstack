#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import logging
import traceback

import tornado
import tornado.web
import tornado.escape
import tornado.locale



class BaseController(tornado.web.RequestHandler):

	# --- application reflect property ---

	@property
	def cache(self):
		return self.application.cache # redis

	@property
	def database(self):
		return self.application.database # postgresql

	# --- enhance controller method ---

	@property
	def is_json(self):
		"""Check request with "application/json": "application/json"(default).
		"""
		headers = {
			"text/json": "text/json",
			"text/javascript": "text/javascript",
			"application/json": "application/json", # default
			"application/javascript": "application/javascript",
		}
		try:
			name = self.request.headers.get("Content-Type")
			return name == headers[name.get("Content-Type", "")]
		except Exception, exception:
			logging.error("json check: " + str(exception))

	@property
	def json_args(self):
		"""Parse json post json_arguments for `RequestHandler`.
		"""
		if not hasattr(self, "_json_args") and self.is_json():
			try:
				self._json_args = tornado.escape.json_unescape(self.request.body)
			except Exception, exception:
				logging.error("json_args: " + str(exception))
		return self._json_args

	def json_arg(self, name, default=[], strip=True):
		return self.json_args.get(name, default).strip() if strip else self.json_args.get(name, default)

	@property
	def is_ajax(self):
		"""Check request with XmlHttpRequest.
		"""
		return self.request.headers.get("X-Requested-With", "").lower() == "xmlhttprequest"

	# --- tornado override method ---

	# def initialize(self):
	#     pass

	# def prepare(self):
	#     pass

	def on_finish(self):
		pass

	def on_connection_close(self):
		pass

	def get_login_url(self):
		# return super(BaseController, self).get_login_url()
		return self.reverse_url("login")

	def get_current_user(self):
		session = self.get_secure_cookie("session")
		return self.backend.get_current_user(session) if session else None

	def get_user_locale(self):
		if self.get_argument("locale", None):
			return tornado.locale.get(self.get_argument("locale")) # UrlQueryString
		else:
			if self.current_user:
				return tornado.locale.get(self.current_user.locale) # User Prefs
			elif self.get_cookie("locale", None):
				return tornado.locale.get(self.get_cookie("locale")) # Cookie Prefs
			else:
				return self.get_browser_locale() # Browser Locale Detections

	def write_error(self, status_code, **kwargs):
		"""Override `write_error` or `get_error_html` method. Use `send_error`.
		"""
		if self.settings.get("debug") and "exe_info" in kwargs:
			return super(BaseController, self).write_error(status_code, **kwargs)
		else:
			self.set_status(status_code)
			return self.render("error.html", 
				status_code=status_code,
				status_message=httplib.responses[status_code],
				custom_message=kwargs.get("custom_message", None))

	def render_string(self, template_name, **kwargs):
		"""Hooks inner use `template_vars` for template.
		"""
		template_vars = self.template_vars if self.template_vars else dict()
		kwargs.update(template_vars)
		return super(BaseController, self).render_string(template_name, **kwargs)

	def get_template_namespace(self):
		return super(BaseController, self).get_template_namespace()

	# --- default headers ---

	def set_default_headers(self):
		self.set_header("Server", "AppstackServer/%s" % tornado.version)
		self.set_header("X-Frame-Options", "deny")
		self.set_header("X-XSS-Protection", "1;mode=block")


class ErrorController(BaseController):
	def prepare(self, status_code=404, **kwargs):
        if self.settings.get("debug", False) is not True:
            pass
        else:
            pass
        self.set_status(status_code)
        status_code = status_code
        status_message = httplib.responses[status_code]
        custom_message = kwargs.get('custom_message', None)
        return self.render("error.html", 
        	status_code=status_code, 
        	status_message=status_message, 
        	custom_message=custom_message)


class IndexController(BaseController):
	def get(self):
		return self.render("index.html")