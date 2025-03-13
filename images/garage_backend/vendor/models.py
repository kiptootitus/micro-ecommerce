from django.contrib.auth.models import User
from django.db import models
from garage.models import BaseModel
from utils import generate_unique_id
from config_master import OPTIONAL_FIELDS


class Vendor(BaseModel):
    """
    This model contains fields that are available in all the models
    """
    id = models.CharField(max_length=100, primary_key=True, default=generate_unique_id, editable=False)
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

    def __str__(self):
        user_name = self.user.username if self.user else "No User"
        business_type = self.business_type_name if self.business_type_name else "No Business Type"
        return f"Vendor - {user_name} - ({business_type})"

    def is_fully_filled(self):
        """ Checks if all the fields have been filled """
        return [field.name for field in self._meta.get_fields() if field.name not in OPTIONAL_FIELDS and not getattr(self, field.name)]
