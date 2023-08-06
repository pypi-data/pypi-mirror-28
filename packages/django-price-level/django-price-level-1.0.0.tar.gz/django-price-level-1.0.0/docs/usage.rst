=====
Usage
=====

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
