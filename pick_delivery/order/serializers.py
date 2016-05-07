from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    pickup_time = serializers.DateTimeField(input_formats=["%Y-%m-%d %I:%M %p",])
    dropoff_time = serializers.DateTimeField(input_formats=["%Y-%m-%d %I:%M %p",])
    status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ('owner', 'pickup_addr', 'contact_name', 'phone', 'pickup_time', 'dropoff_time', 'items', 'payment_type', 'status')
