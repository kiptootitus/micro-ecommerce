from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, user_email, password=None, **extra_fields):
        if not user_email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(user_email)
        user = self.model(user_email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, password=None, **extra_fields):
        extra_fields.setdefault('is_administrator', True)
        return self.create_user(user_email, password, **extra_fields)


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=100, unique=True)
    registration_date = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_administrator = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'user_email'

    def __str__(self):
        return self.user_email


class Address(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)


class Profile(models.Model):
    USER_ROLE_CHOICES = [('user', 'User'), ('admin', 'Admin')]  # Example choices
    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=255, choices=USER_ROLE_CHOICES, default='user')
    phone = PhoneNumberField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_email} ({self.role})"
