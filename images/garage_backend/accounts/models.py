from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField

from config_master import USER_ROLE_CHOICES, USER_ROLE
from garage.models import BaseModel


# Create your models here.
class SendMail:
    pass


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    SendMail().send_password_reset_email({'reset_password_token': reset_password_token})


class Address(BaseModel):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)



class Profile(BaseModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=255, choices=USER_ROLE_CHOICES, default=USER_ROLE)
    phone = PhoneNumberField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='profiles')

    def __str__(self):
        return '%s (%s)' % (self.user.username, self.role)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    This is a signal that is called when saving a user object, and it updates the profile of the user.
    :param sender:
    :param instance: The user object that is being saved
    :param kwargs:
    :return: None
    """
    Profile.objects.get(user=instance).save()


class Contact(BaseModel):
    """
    This holds address information of a user
    """
    name = models.CharField(max_length=500, null=False, blank=False, )
    email = models.EmailField(null=False, blank=False, unique=True)

