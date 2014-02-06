#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
# database schema defination
# 

import datetime
import os.path
import sys

import sqlalchemy

from sqlalchemy import (
	Column, Index,
	DateTime, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import (
	ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, 
	DOUBLE_PRECISION, ENUM, FLOAT, INET, INTEGER, 
	INTERVAL, MACADDR, NUMERIC, REAL, SMALLINT, TEXT, TIME, 
	TIMESTAMP, UUID, VARCHAR
)

try:
	import appstack
except ImportError:
	APPSDIR = os.path.realpath('..')  # /appstack/database
	BASEDIR = os.path.join(APPSDIR, '..') # /appstack
	sys.path.append(BASEDIR) # /appstack

import appstack
import appstack.applications
import appstack.database
import appstack.settings

import appstack.applications.application

# db shortcut
database = appstack.applications.application.database


SCHEMA_VERSION = '20131117165023' # Year Month Day Hour Minutes Second

DATABASE_ENGINE = 'postgresql'
DATABASE_DRIVER = 'psycopg2'
