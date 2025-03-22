from rest_framework import serializers

from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['user', 'business_name', 'email', 'is_active', 'country_of_issue', 'phone_number', 'identity_number',
                  'country_of_citizenship', 'date_of_birth', 'date_of_expiry', 'date_of_issue', 'business_type_name']
