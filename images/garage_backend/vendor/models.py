from django.db import models
from  garage.models import BaseModel
# Create your models here.

class Vendor(BaseModel.model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'vendor'
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class VendorManager:
    def get_vendor_by_email(self, data: dict) -> Vendor:
        """
        This method returns a vendor by email
        :param data: {
            'email': The email value,
        }
        :return: Vendor
        """
        return Vendor.objects.get(email=data['email'])

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def get_email(self):
        return self.email
