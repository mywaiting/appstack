#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. _WTForms: http://wtforms.simplecode.com

# Wrapper with WTForms for Tornado as Form.

Basically we only need to map the request handler's `arguments` to the 
`wtforms.form.Form` input. Quick example::

	from wtforms import TextField, validators
	from tornadotools.forms import BaseForm

	class SampleForm(BaseForm):
		username = TextField('Username', [
			validators.Length(min=4, message="Too short")
			])

		email = TextField('Email', [
			validators.Length(min=4, message="Not a valid mail address"),
			validators.Email()
			])

Then, in the `RequestHandler`::

	def get(self):
		# pass vars: self.request.arguments, self.locale_code
		form = SampleForm(self)
		if form.validate():
			# do something with form.username or form.email
			pass
		self.render('template.html', form=form)
"""

import wtforms


class Form(wtforms.Form):

	def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
		self._handler = formdata
		super(Form, self).__init__(TornadoRequestWrapper(self._handler), obj=obj, prefix=prefix, **kwargs)

	def _get_translations(self):
		# use `Tornado.web.RequestHandler.locale`
		return TornadoLocaleWrapper(self._handler.locale)


class TornadoRequestWrapper(object):

	def __init__(self, handler):
		self._handler = handler

	def __iter__(self):
		return iter(self._handler.request.arguments)

	def __len__(self):
		return len(self._handler.request.arguments)

	def __contains__(self, name):
		return (name in self._handler.request.arguments)

	def getlist(self, name):
		# use `Tornado RequestHandler.get_arguments()`
		return self._handler.get_arguments(name)


class TornadoLocaleWrapper(object):

	def __init__(self, locale):
		self.locale = locale

	def gettext(self, message):
		return self.locale.translate(message) if self.locale else message

	def ngettext(self, message, plural_message, count):
		return self.locale.translate(message, plural_message, count) if self.locale else message