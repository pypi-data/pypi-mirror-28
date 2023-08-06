Django GraphQL GeoJSON
======================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

`GeoJSON`_ support for `Django GraphQL`_

.. _GeoJSON: http://geojson.org
.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-geojson --process-dependency-links


GeoJSONType
-----------

.. code:: python

    from graphql_geojson.types import GeoJSONType


    class PlaceType(GeoJSONType):

        class Meta:
            model = models.Place
            geojson_field = 'location'


Here we go!

.. code::

    query {
      places {
        id
        type
        geometry {
          type
          coordinates
        }
        properties {
          name
        }
      }
    }



.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-geojson.svg
   :target: https://pypi.python.org/pypi/django-graphql-geojson

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-geojson.svg
   :target: https://pypi.python.org/pypi/django-graphql-geojson

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-geojson.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-geojson

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-geojson.svg
   :target: https://codecov.io/gh/flavors/django-graphql-geojson

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/67dbb917ad4cf8c422a6/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-geojson


