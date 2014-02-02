#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
# database schema defination
# 

import datetime
import os.path
import sys.path

import sqlalchemy

from sqlalchemy import (
	Column, Index,
	DateTime, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import (
	ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, 
	DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, 
	INTERVAL, MACADDR, NUMERIC, REAL, SMALLINT, TEXT, TIME, 
	TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, 
	DATERANGE, TSRANGE, TSTZRANGE
)

try:
	import appstack
except ImportError:
	APPSDIR = os.path.realpath('..')  # /appstack/database
	BASEDIR = os.path.join(APPSDIR, '..') # /appstack
	sys.path.append(BASEDIR) # /appstack

import appstack
import appstack.application
import appstack.database
import appstack.settings


# db shortcut
database = appstack.application.main.database


SCHEMA_VERSION = '20131117165023' # Year Month Day Hour Minutes Second

DATABASE_ENGINE = 'postgresql'
DATABASE_DRIVER = 'pycopg2'
