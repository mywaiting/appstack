![appstack](https://raw.github.com/mywaiting/appstack/master/appstack/applications/assets/images/logo.png)

----------


# Appstack

Appstack is a web application skeleton for python web development.

It design for [Tornado](http://www.tornadoweb.org "tornado web framework") web application, just a skeleton.

# Usage

	$ python /your/path/appstack/applications/application.py --port=8000

Open your browser and input url as [http://localhost:8000/](http://localhost:8000/), you will see hello world.

If you need database support, you need to modify this source code and enjoy it!

# Requirement

This skeleton build on some awesome python package. lists as follow:

* [Tornado](http://www.tornadoweb.org "tornado web framework")
* [SQLAlchemy](http://www.sqlalchemy.org/ "SQLAlchemy ORM framework")
* [WTForms](http://wtforms.simplecodes.com/ "WTForms")

Especially, recommand [Postgresql](http://www.postgresql.org "postgresql") as primary data store and [Redis](http://redis.io "redis") as secondary data store or just as cache. and you need more requirements.

* [Redis](https://pypi.python.org/pypi/redis/ "redis python client")
* [Psycopg](http://initd.org/psycopg/ "posgresql python client - psycopg")

# Contribute

If you have any questions or find some bug. please pull the request and notify me. I will merge your contribute into the master depends on project. Thank you.