#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from redis import StrictRedis

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import appstack
import appstack.applications

from appstack.applications.application import cache, database


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


class Redis(object):
	# urls: default://host:port/cache
	# urls: socket://socket_path
	def __init__(self, urls):
		if urls.startwith("default"):
			options = self._parse_urls(urls)
			return StrictRedis(host=options['host'], port=options['port'], db=options.database)
		elif urls.startwith("socket"):
			options = self._parse_socket_urls(urls):
			return redis.Redis(unix_socket_path=options.unix_socket_path)
		else:
			raise exc.ArgumentError("Redis URLs Error.")

	# urls: default://host:port/cache
	def _parse_urls(self, urls):
		pattern = re.compile(r"""
			(?P<name>[\w\+]+)://
			(?:
				(?:
					\[(?P<ipv6host>[^/]+)\] |
					(?P<ipv4host>[^/:]+)
				)?
				(?::(?P<port>[^/]*))?
			)?
			(?:/(?P<database>.*))?
			""", re.X)

		m = pattern.match(urls)
		if m is not None:
			componets = m.groupdict()
			ipv4host = componets.pop('ipv4host')
			ipv6host = componets.pop('ipv6host')
			componets['host'] = ipv4host or ipv6host
		else:
			raise exc.ArgumentError("Redis URLs Error.")

		return componets

	# urls: socket://socket_path
	def _parse_socket_urls(self, urls):
		pattern = re.compile(r"""
			(?P<name>[\w\+]+)://
			(?P<unix_socket_path>.*)?
			""", re.X)

		m = pattern.match(urls)
		if m is None:
			raise exc.ArgumentError("Redis URLs Error.")

		return componets
		


"""Model class for all Models to initialize as Backend.
"""

class BaseModelMetaClass:
	pass


class BaseModel:
	"""所以的Model都必须继承自BaseModel，以便调用其中的cache和database变量
	"""
	# 初始化导入Class的方法集合
	__metaclass__ = BaseModelMetaClass

	# 新建类时导入数据库变量
	def __new__(cls):
		cls.cache = cache
		cls.database = database

	def __init__(self):
		"""直接返回self方便链式调用。
		UsersModel().create(......)
		UsersModel().update(......)
		"""
		return self