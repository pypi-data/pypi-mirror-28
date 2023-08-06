============================
django-cdc
============================

Tracking changes in django models and push it to logger/aws endpoints.


Quickstart Guide
===============================

Install it with pip from PyPi::

    pip install django-cdc

before installing djangoCDC, make sure that you have already run the following command or
your environment the following packages:

   pip install psycopg2
   pip install django-bitfield
   pip install boto3
   pip install pyyaml
   pip install django-extensions
   pip install confluent-kafka

Add ``django_cdc`` to your ``INSTALLED_APPS``::
   INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_cdc',
)

If you want to track full model changes, then you need to attach an ``DjangoCDC`` manager to the model.
For foreign key attributes, we need to pass kwargs foreign of dict type and partition_key is only used with kafka::

    from django.db import models
    from django_cdc.models.managers import DjangoCDC
    from django_cdc.models.constants import ServiceType


    class ProductCategory(models.Model):
        name = models.CharField(max_length=150, primary_key = True)
        description = models.TextField()
        django_cdc = DjangoCDC(services=[ServiceType.SNS], partition_key=name)

    class Product(models.Model):
        name = models.CharField(max_length = 150)
        description = models.TextField()
        price = models.DecimalField(max_digits = 10, decimal_places = 2)
        productcategory = models.ForeignKey(ProductCategory)
        django_cdc = DjangoCDC(foreign_keys={'productcategory':['name','description']},services=[ServiceType.SNS,ServiceType.KINESIS])

ServiceType is used for specifying on which you want to publish.

Run the following commmand to deploy lambda function that pushes data to kinesis:
        python manage.py setservice

By default warn, error, critical logging level are enabled.

To enable info logging:
        python manage.py setservice --logging_level=info

To enable debugging:
        python manage.py setservice --logging_level=debug

Following fields handled for json serialization:
        BitHandler
        datetime
        time
        ImageFieldFile

