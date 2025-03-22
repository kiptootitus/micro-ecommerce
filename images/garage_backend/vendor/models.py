from django.conf import settings
from django.db import models

from config_master import OPTIONAL_FIELDS
from garage.models import BaseModel
from utils import generate_unique_id


class Vendor(BaseModel):
    """
    This model contains fields that are available in all the models
    """
    id = models.CharField(max_length=100, primary_key=True, default=generate_unique_id, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

    def __str__(self, *args, **kwargs):
        return f" {self.user}  ({self.business_type_name})"

    def is_fully_filled(self):
        """ Checks if all the fields have been filled """
        return [field.name for field in self._meta.get_fields() if
                field.name not in OPTIONAL_FIELDS and not getattr(self, field.name)]
