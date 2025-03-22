from rest_framework import serializers

from .models import Users, Address, Profile


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zip_code']


class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Profile
        fields = ['role', 'phone', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        profile = Profile.objects.create(address=address, **validated_data)
        return profile

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()

        instance.role = validated_data.get('role', instance.role)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    address = AddressSerializer(source='profile.address', read_only=True)

    class Meta:
        model = Users
        fields = ['user_id', 'email', 'registration_date', 'last_login',
                  'is_administrator', 'is_active', 'email_verified', 'profile', 'address']
        read_only_fields = ['registration_date', 'last_login']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data.get('password')
        )
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save(user=user)
        return user
