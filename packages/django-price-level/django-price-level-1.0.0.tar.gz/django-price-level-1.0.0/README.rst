=============================
django-price-level
=============================

.. image:: https://badge.fury.io/py/django-price-level.png
    :target: https://badge.fury.io/py/django-price-level

.. image:: https://travis-ci.org/PetrDlouhy/django-price-level.png?branch=master
    :target: https://travis-ci.org/PetrDlouhy/django-price-level

Adds time limited price levels to your model class.

Documentation
-------------

The full documentation is at https://django-price-level.readthedocs.io.

Quickstart
----------

Install django-price-level::

    pip install django-price-level

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'price_level',
        ...
    )

Configure in your settings the desired model:

.. code-block:: python

   from model_utils import Choices
   PRICE_LEVEL_MODEL = 'your.Model'
   PRICE_LEVEL_CATEGORY_CHOICES = Choices(('basic', _('Basic')), ('company', _('For companies')))
   PRICE_LEVEL_CATEGORY_DEFAULT = 'basic'

Add author middleware in settings:

.. code-block:: python

  MIDDLEWARE_CLASSES = [
      ...
      'author.middlewares.AuthorDefaultBackendMiddleware',
      ...
   ]

Use `Pricable` behavioral mixin to your model:

.. code-block:: python

   from price_level.models import Pricable
   class Model(Pricable, models.Model):
      ...
   
Now you can get current price for your category:

.. code-block:: python

     price_level = model.get_current_price_level(category='company')

Features
--------

* Adds PriceLevel models can be bound to your model class

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
