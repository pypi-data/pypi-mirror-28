django-tastypie-mongoengine
===========================

This Django application provides MongoEngine_ support for django-tastypie_.

**This project is unmaintained. If anyone wants to step up and take over maintenance, please open an issue.**

Django 1.9+ compatibility fixes
-------------------------------

* Fixed 'self._meta.queryset.query.query_terms' to return a set instead of dictionary as according to django-tastypie 0.13.3.
* Replaced 'SortedDict' with 'collections.OrderedDict' since SortedDict is deprecated as of Django 1.7 & removed in Django 1.9.
* In the method 'get_fields' of class 'MongoEngineResource', help_text of field is being retrieved which might not be present. Replaced with conditional retrieval.

Requirements
------------

* Python_ 2.7+
* Django_ 1.9+
* django-tastypie_ 0.13.3+
* MongoEngine_ 0.10.6+

.. _Python: https://python.org
.. _Django: http://djangoproject.com
.. _django-tastypie: https://github.com/toastdriven/django-tastypie
.. _MongoEngine: http://mongoengine.org

How to use?
-----------

* See documentation: http://django-tastypie-mongoengine.readthedocs.org
* See usage in tests: http://github.com/wlanslovenija/django-tastypie-mongoengine/tree/master/tests
