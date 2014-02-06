#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Wrapper with WTForms for Tornado as Form.
"""

import re

import wtforms
import wtforms.form
import wtforms.fields
import wtforms.widgets
import wtforms.validators

import tornado
import tornado.escape
import tornado.locale



class BaseForm(wtforms.Form):
	def __inti__(self, formdata=None, obje=None, prefix='', locale_code='en_US', **kwargs):
		self._locale_code = locale_code
		super(BaseForm, self).__inti__(formdata, obj, prefix, **kwargs)

	def process(self, formdata=None, obj=None, **kwargs):
		if formdata is not None and not hasattr(formdata, 'getlist'):
			formdata = TornadoArgumentsWrapper(formdata)
		super(BaseForm, self).process(formdata, obj, **kwargs)

	def _get_translations(self):
		if not hasattr(self, '_locale_code'):
			self._locale_code = 'en_US'
		return TornadoLocaleWrapper(self._locale_code)


class TornadoArgumentsWrapper(dict):
	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError:
			raise AttributeError

	def __setattr__(self, name, value):
		self[name] = value

	def __delattr__(self, name):
		try:
			del self[name]
		except KeyError:
			raise AttributeError

	def getlist(self, name):
		try:
			values = []
			for v in self.get(name, []):
				v = tornado.escape._unicode(v)
				if isinstance(v, unicode):
					v = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", v)
				values.append(v)
			return values
		except KeyError:
			raise AttributeError


class TornadoLocaleWrapper(object):
	def __init__(self, code):
		self.locale = tornado.locale.get(code)

	def gettext(self, message):
		return self.locale.translate(message)

	def ngettext(self, message, plural_message, count):
		return self.locale.translate(message, plural_message, count)