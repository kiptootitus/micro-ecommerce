from datetime import datetime

from django.db import models

from config_master import TZ
from utils import generate_random_string
from .middleware import get_current_user


# Create your models here.
class BaseModel(models.Model):
    """
    This model contains fields that are available in all the models
    """
    created_datetime = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=500, default='', null=True)
    modified_datetime = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.CharField(max_length=500, default='', null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        current_user = get_current_user()

        if current_user:
            username = current_user.username
            if not self.created_by:
                self.created_by = username
            else:
                self.modified_by = username
        super(BaseModel, self).save(*args, **kwargs)


def unique_id_generator(id_string: str = None) -> str:
    """
    Generates a unique id
    :param id_string:
    :return:
    """
    if id_string:
        id_string_split = id_string.split('-')
        increment_value = id_string_split[-1]
        increment_value = int(increment_value) + 1
        return f'{str(id_string_split[0])}-{str(increment_value)}'
    now = datetime.now(TZ)
    time_string = now.strftime("%Y%d%m%d%H%M%S")
    return f'{time_string}{str(generate_random_string(4))}-0'


def generate_unique_id(instance) -> str:
    """
    Generates a unique id for a model object
    :param instance: A models.Model object instance
    :return: The unique Id
    """
    unque_id = unique_id_generator().upper()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(id=unque_id).exists()
    if qs_exists:
        return generate_unique_id(instance)
    return unque_id
