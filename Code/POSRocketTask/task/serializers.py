from .models import *
from rest_framework import serializers


class AmountSerializer(serializers.Serializer):
    model = AmountModel
    fields = ('amount', 'currency')


class DataSerializer(serializers.Serializer):
    applied_money = AmountSerializer

    class Meta:
        model = DataModel
        fields = ('id', 'name', 'rate', 'inclusion_type', 'is_custom_amount', 'applied_money')


class MainSerializer(serializers.ModelSerializer):
    taxes = DataSerializer(read_only=True, many=True)

    class Meta:
        model = AllDataModel
        fields = ('_id', 'business_id', 'location_id', 'transaction_id', 'receipt_id', 'serial_number', 'dining_option',
                  'creation_time', 'taxes')


