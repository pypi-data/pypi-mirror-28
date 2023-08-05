=====
Django-bugout
=====
Django-bugout is a awesome app to allow us can view "full debug info" from frontend in Production server, which set DEBUG=False.
Everything output exactly the same with case of DEBUG=True

Quick start
-----------

1. Add "django_bugout" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_bugout',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('django_bugout/', include('django_bugout.urls')),

3. Change your settings.py to DEBUG=False
4. Start the development server and visit http://127.0.0.1:8000/django_bugout
   to input what page you want examine.

   Sample:
	/myweb/someapi/
   Note: URI input must not allow domain & protocol

========================================================================================
