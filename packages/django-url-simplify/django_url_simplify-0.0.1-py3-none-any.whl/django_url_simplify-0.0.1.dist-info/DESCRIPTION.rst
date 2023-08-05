=====
Url Simplify
=====

Url Simplify is a simple Django app which generates simplified base62 urls
from regular ones.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add ``url_simplify`` to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'url_simplify',
    ]

2. Include the ``url_simplify`` URLconf in your project urls.py like this::

    path('url_simplify/', include('url_simplify.urls')),

3. Run `python manage.py migrate` to create the url_simplify models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a url_simplify (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/url_simplify/ to start generating simplified urls.


