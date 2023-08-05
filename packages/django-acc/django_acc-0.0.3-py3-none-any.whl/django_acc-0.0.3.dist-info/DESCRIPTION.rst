DON'T USE ME. I'M BEING USED INTERNALLY ONLY.

Django-acc: Another reusable Django account management application

Installation
============

``pip install django-acc``

Requirements
============

django >= 2.0 djangorestframework >= 3.7.7 'rest\_framework',

Configurations
==============

settings.py
-----------

-  Add ``rest_framework`` to INSTALLED\_APPS
-  Add ``accounts`` to INSTALLED\_APPS

urls.py
-------

-  Add ``path('accounts', include('accounts.urls'))`` to ``urlpatterns``
   in your project's ``urls.py``

Templates
---------

-  Make sure that you have a ``base.html`` templates



