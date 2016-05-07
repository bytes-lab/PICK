from rest_framework import serializers, exceptions
from .models import *


class UserDetailsSerializer(serializers.ModelSerializer):

    """
    Sender model w/o password
    """
    class Meta:
        model = Sender
        fields = ['first_name', 'last_name', 'gender', 'email', 'address', 'store_url', 'package_type', 'phone']
        read_only_fields = ('email', )
