=====
Creh Pages
=====

Creh-pages is a simple Django app allow you to manage sections of
your django pages quickly and by any administrator user

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. creh-pages can be obtained directly from PyPI, and can be installed with pip:

    pip install crehpages

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'pages',
    ]

2. Run "python manage.py migrate" to create the log models.

3. Use



--- Upload

python runtests.py
python setup.py sdist upload -r pypi
twine upload dist/*