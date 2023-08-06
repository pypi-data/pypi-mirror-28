=====
Weboffice 365
=====

Weboffice 365 is a advanced Django app to manage and organise business process.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "weboffice365" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'weboffice365',
    ]

2. Include the weboffice365 URLconf in your project urls.py like this::

    path('', include('weboffice365.urls')),

3. Run `python manage.py migrate` to create the weboffice365 models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to manage your organisation. (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/