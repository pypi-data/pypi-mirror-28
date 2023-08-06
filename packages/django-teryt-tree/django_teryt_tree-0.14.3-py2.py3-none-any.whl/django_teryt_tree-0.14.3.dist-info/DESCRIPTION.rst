=============================
django-teryt-tree
=============================

.. image:: https://badge.fury.io/py/django-teryt-tree.png
    :target: https://badge.fury.io/py/django-teryt-tree

.. image:: https://travis-ci.org/ad-m/django-teryt-tree.png?branch=master
    :target: https://travis-ci.org/ad-m/django-teryt-tree

.. image:: https://coveralls.io/repos/ad-m/django-teryt-tree/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ad-m/django-teryt-tree?branch=master 

Django-teryt-tree is a Django app that implements TERYT database as tree by django-mptt and flat SIMC database.

Documentation
-------------

The full documentation is at https://django-teryt-tree.readthedocs.org.

Quickstart
----------

Install django-teryt-tree::

    pip install django-teryt-tree


Then add to INSTALLEDA__APPS::

    INSTALLED_APPS+=('teryt_tree')

Then use it in a project::

    import teryt_tree

or::

    from teryt_tree.models import JednostkaAdministracyjna

To load TERC register database visit http://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default to download valid database. Next to execute following commands::

    pip install lxml
    python manage.py load_teryt --input TERC.xml

To load SIMC register download valid database. Next to execute following commands::

    python manage.py load_simc --input SIMC.xml

Features
--------

* Import database from official exports - TERC and SIMC database.
* Store data as modified pre-order traversal tree for effective regional query
* Support format of teryt.stat.gov.pl and eteryt.stat.gov.pl

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage




History
-------

0.14.0 (2017-08-15)
*******************

* Fix update of SIMC registry
* Fix compatibility of ``teryt_tree.est_framework_ext.viewsets.JednostkaAdministracyjnaFilter``
* Add new format od TERC export

0.13.2 (2017-08-11)
*******************

* Temporary drom SIMCSerializer

0.13.1 (2017-08-11)
*******************

* Fix django-filters compatibility in ``dal_ext``.

0.13.0 (2017-07-13)
*******************

* Improve import performacne
* Fix path of *.xml files (use on-premise TravisCI-cached copy)
* Add support to SIMC database

0.12.1 (2017-04-04)
*******************

* Improve compatibility django-filters 1.x in ``dal_ext``

0.12.0 (2017-04-04)
+++++++++++++++++++

* Move ``teryt_tree.filters`` to ``teryt_tree.filters_ext.filters``
* Fix compatibility django-filters 1.x in ```filters_ext``

0.11.0 (2016-09-13)
+++++++++++++++++++
* Add locale to package

0.10.0 (2016-09-13)
+++++++++++++++++++
* Add missing migrations
* Add dummy urlpatterns

0.9.0 (2016-09-13)
++++++++++++++++++
* Fix runtests

0.8.0 (2016-12-10)
++++++++++++++++++
* Add bumpversion
* Add AppConfig with translation ``app_label``
* Update polish locale
* Extract settings as standalone file
* Add manage.py

0.7.0 (2016-09-13)
++++++++++++++++++
* Drop django 1.7 support
* Add support django 1.10
* Add ``--limit`` param to ``load_teryt`` command

0.6.0 (2016-07-03)
++++++++++++++++++

* Add django-rest-framework extensions
* Add django-autocomplete-light v3 support
* Add JednostkaAdministracyjnaQuerySet.area
* Add one-line TERC import command
* Add cache to Travis
* Fix syntax in HISTORY.rst


0.5.0 (2016-04-14)
++++++++++++++++++

* Added TravisCI badge in README.rst
* Added download_url in setup.py

0.4.0 (2016-04-14)
++++++++++++++++++

* Remove PassThroughManagerMixin

0.1.0 (2015-10-02)
++++++++++++++++++

* First release on PyPI.


