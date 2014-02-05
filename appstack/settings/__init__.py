#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Redis
cache_driver="default" # default/socket
cache_host="localhost"
cache_name=""
cache_port=6379 # for Redis

# Posgresql
database_driver="postgresql" # Posgresql
database_host="localhost"
database_name=""
database_password=""
database_port=5432 # for Posgresql
database_username=""

# Tornado
cookie_secret=""
debug=True
static_path=None
template_path=None
xsrf_cookies=True

# Aka. settings
settings=None

# Server
port=8000 # run backend server on the given port
processor=1 # run backend server with the processors







# 
# import other settings for different environment
# 

try:
    from .develop_settings import * # DevelopSettings
except ImportError:
    pass


try:
    from .production_settings import * # ProductionSettings
except ImportError:
    pass


try:
    from .local_settings import * # LocalSettings
except ImportError:
    pass