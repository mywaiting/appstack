#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import appstack
import appstack.applications
import appstack.database

# from appstack.applications.application import cache, database
# from appstack.database import schema, seeds


"""Wrapper with SQLAlchemy for Tornado as Model.
"""

class SQLAlchemy(object):
	def __init__(self, engine, **kwargs):
		self.engine = create_engine(engine, **kwargs)
		self.session = scoped_session(sessionmaker(bind=self.engine))

	@property
	def Model(self):
		if hasattr(self, "_base"):
			base = self._base
		else:
			base = declarative_base(name='Model')
			self._base = base
			base.query = self.session.query_property()
		return base

	def create_all(self):
		self.Model.metadata.create_all(bind=self.engine)

	def drop_all(self):
		self.Model.metadata.drop_all(bind=self.engine)