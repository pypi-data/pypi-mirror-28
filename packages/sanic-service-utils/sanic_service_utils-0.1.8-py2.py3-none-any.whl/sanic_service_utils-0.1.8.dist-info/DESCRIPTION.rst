========================================
Utils for sanic microservice development
========================================

.. image:: https://img.shields.io/pypi/v/sanic-service-utils.svg
        :target: https://pypi.python.org/pypi/sanic-service-utils
.. image:: https://img.shields.io/pypi/l/sanic-service-utils.svg
        :target: https://pypi.python.org/pypi/sanic-service-utils



:code:`sanic-service-utils` set of utils to use with sanic framework

Installation
------------

:code:`sanic-service-utils` is available as a python library on Pypi. Installation is very simple using pip :

.. code:: bash

    $ pip install sanic-service-utils

This will install :code:`sanic-service-utils` as well as external dependency.

Basic usage
-----------

Basically :code:`sanic-service-utils` is just set of blueprints for sanic and additional stuff. You should name you app correctly to use this set.

Blueprints
-----------------


All blueprints can be found in :code:`listeners` module.

:anji_orm_configuration: Basically, setup :code:`register` when you start app and stop it, when you stop app. Blueprint use variables :code:`RETHINKDB_HOST`, :code:`RETHINKDB_PORT`, :code:`RETHINKDB_DATABASE`, :code:`RETHINKDB_USERNAME`, :code:`RETHINKDB_PASS`from configuration to configure register.
:sentry_configuration: Configure sentry for web server, use variable :code:`SENTRY_DSN` from configuration.
:backgroun_task_configuration: Set empty list like variable :code:`tasks_list` to sanic app that will be cancelled on server stop. Please, use listener :code:`after_server_start` to add new tasks.
:aiohttp_session_configuration: Just configure aiohttp settion like :code:`async_session` variable for app.
:jinja_session_configuration: Just configure jinja render system like :code:`jinja` variable for app.
:log_configuration: Just configure logging for app by app name.
:sanic_session_configuration: Configure sanic session plugin, you should add variable :code:`session_interface` with SessionIntreface object to sanic app object.

