==================
Django Materialize
==================

Django Materialize is a simple Django app to include Materialize into your project.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "materialize" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'materialize',
    ]

2. To use materialize in your templates you should extend them from materialize_base.html for production,
    materialize_base_dev.html - for development, or include Materialize static files manually.
    Templates are placed in materialize directory and static files in materialize/(css | js | fonts).
