#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from .schema import *

from plustack.apps.models.user import User
from plustack.apps.models.plan import Plan


# plans
plan = Plan()
plan.create(name='basic-monthly', price=3)
plan.create(name='basic-yearly', price=30)

# users
user = User()
user.create(mail='admin@plustack.com', password='passw0rd')



if __name__ == '__main__':
	print 'Seeds to Initialize Database...'