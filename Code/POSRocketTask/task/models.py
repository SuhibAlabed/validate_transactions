from __future__ import unicode_literals
from django.db import models
import uuid


class DataModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    rate = models.FloatField()
    inclusion_type = models.CharField(max_length=255)
    is_custom_amount = models.BooleanField()


class AmountModel(models.Model):
    amount = models.IntegerField()
    currency = models.CharField(max_length=255)


class AllDataModel(models.Model):
    _id = models.CharField(max_length=255)
    business_id = models.CharField(max_length=255)
    location_id = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    receipt_id = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    dining_option = models.CharField(max_length=255)
    creation_time = models.CharField(max_length=255)

