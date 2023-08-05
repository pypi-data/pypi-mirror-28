===================
RethinkDB-based ORM
===================

.. image:: https://img.shields.io/pypi/v/anji-orm.svg
        :target: https://pypi.python.org/pypi/anji-orm
.. image:: https://img.shields.io/pypi/l/anji-orm.svg
        :target: https://pypi.python.org/pypi/anji-orm
.. image:: https://gitlab.com/AnjiProject/anji-orm/badges/master/build.svg
        :target: https://gitlab.com/AnjiProject/anji-orm



:code:`anji_orm` simple ORM for RethinkDB

Installation
------------

:code:`anji_orm` is available as a python library on Pypi. Installation is very simple using pip :

.. code:: bash

    $ pip install anji_orm

This will install :code:`anji_orm` as well as external dependency.

Basic usage
-----------

ORM registry should be initiated before usage:

.. code:: python

    # For sync usage
    register.init(dict(db='test'))
    register.load()

    # Or for async usage

    register.init(dict(db='test'), async_mode=True)
    await register.async_load()

That, create some model

.. code:: python

    class T1(Model):

        _table = 't2'

        a1 = StringField()
        a2 = StringField()

    t2 = T1(a1='b', a1='c')
    t2.send()
    # or for async usage
    await t2.async_send()

