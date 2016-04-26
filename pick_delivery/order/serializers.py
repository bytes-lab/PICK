from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'pickup_addr', 'contact_name', 'phone', 'pickup_time', 'dropoff_time', 'items', 'payment_type',)
