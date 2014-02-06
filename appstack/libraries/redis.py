#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from redis import StrictRedis

import appstack
import appstack.applications
import appstack.database

# from appstack.applications.application import cache, database
from appstack.database import schema, seeds



"""Wrapper with Redis for Access URLs srttings.
"""

class Redis(object):
	# urls: default://host:port/cache
	# urls: socket://socket_path
	def __init__(self, urls):
		if urls.startwith("default"):
			options = self._parse_urls(urls)
			return StrictRedis(host=options['host'], port=options['port'], db=options.database)
		elif urls.startwith("socket"):
			options = self._parse_socket_urls(urls)
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
	