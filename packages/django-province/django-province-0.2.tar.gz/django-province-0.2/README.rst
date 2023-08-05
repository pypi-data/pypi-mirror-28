=====
Province
=====

Province is a simple Django app to show province, town, city and shahrak in Iran with API. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "province" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'province',
    ]

2. Include the province URLconf in your project urls.py like this::

    path('api/v1/province/', include('province.api.urls')),

3. Run `python manage.py migrate` to create the province models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a province (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/v1/province/ to participate in the poll.