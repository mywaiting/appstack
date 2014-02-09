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
import appstack.database

# from appstack.applications.application import cache, database
from appstack.database import schema, seeds
	


"""Model class for all Models to initialize as Backend.
"""

class ModelMetaClass(type):
	# 新建类时导入数据库变量
	def __new__(cls, name, bases, dct):
		"""To avoid modules that mutually import each other.
		Refer: 
		http://docs.python.org/2/faq/programming.html#how-can-i-have-modules-that-mutually-import-each-other
		http://wiki.woodpecker.org.cn/moin/MiscItems/2008-11-25
		"""
		from appstack.applications.application import cache, database

		cls.cache = cache
		cls.database = database

	 def __init__(cls, name, bases, dct):
	 	pass


class Model:
	"""所以的Model都必须继承自BaseModel，以便调用其中的cache和database变量
	"""
	# 初始化导入Class的方法集合
	__metaclass__ = BaseModelMetaClass

	def __init__(self):
		pass