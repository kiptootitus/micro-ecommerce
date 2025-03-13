from django.contrib.auth.models import User
from django.db import models

from config_master import OPTIONAL_FIELDS
from garage.models import BaseModel, generate_unique_id


# Create your models here.

class Vendor(BaseModel):
    """
    This model contains fields that are available in all the models
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='vendor')
    business_name = models.CharField(max_length=100, default='', null=True)
    email = models.EmailField(max_length=100, default='', null=True)
    is_active = models.BooleanField(default=True)
    country_of_issue = models.CharField(max_length=100, default='', null=True)
    phone_number = models.CharField(max_length=100, default='', null=True)
    identity_number = models.CharField(max_length=100, default='', null=True)
    country_of_citizenship = models.CharField(max_length=100, default='', null=True)
    date_of_birth = models.DateField(null=True)
    date_of_expiry = models.DateField(null=True)
    date_of_issue = models.DateField(null=True)
    business_type_name = models.CharField(max_length=100, default='', null=True)
    id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        user_name = self.user.username if self.user else "No User"
        business_type = self.business_type_name if self.business_type_name else "No Business Type"
        return f"Vendor - {user_name} - ({business_type})"

    def is_fully_filled(self):
        """ Checks if all the fields have been filled """
        fields_names = [f.name for f in self._meta.get_fields()]
        remaining_fields = []
        for field_name in fields_names:
            if field_name in OPTIONAL_FIELDS:
                continue
            try:
                value = getattr(self, field_name)
                if value is None or value == '':
                    remaining_fields.append(field_name)
            except Exception as e:

                continue

        return remaining_fields






