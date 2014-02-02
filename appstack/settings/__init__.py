#!/usr/bin/env python
# -*- coding: utf-8 -*-


debug = True
port = 8000
processor = 1

settings = None

app_static_path = None
app_template_path = None







# 
# import other settings for different environment
# 

try:
    from develop_settings import * # DevelopSettings
except ImportError:
    pass


try:
    from production_settings import * # ProductionSettings
except ImportError:
    pass


try:
    from local_settings import * # LocalSettings
except ImportError:
    pass