DON'T USE ME. I'M BEING USED INTERNALLY ONLY.

Django-acc: Another reusable Django account management application

Installation
============

``pip install django-acc``

Requirements
------------

-  django >= 2.0
-  djangorestframework >= 3.7.7

Configurations
--------------

settings.py
~~~~~~~~~~~

-  Add ``rest_framework`` to INSTALLED\_APPS
-  Add ``django-acc`` to INSTALLED\_APPS

urls.py
~~~~~~~

-  Add ``path('accounts/', include('accounts.urls'))`` to
   ``urlpatterns`` in your project's ``urls.py``

Templates
~~~~~~~~~

-  Make sure that you have a ``base.html`` templates

Features
========

-  Prebuilt ``register``, ``login`` views at ``accounts/register/`` and
   ``accounts/login/``
-  Organization management (WIP)

Concepts
========

*Organization* An organization is a group of accounts. It's optional to
create a new organization, but when a new user is created, a default
organization with the same name is also created.


