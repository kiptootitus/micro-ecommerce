from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def __init__(self):
        super().__init__()
        self.is_superuser = None

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_administrator', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True,)
    email = models.EmailField(max_length=100, unique=True)
    registration_date = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_administrator = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

class Profile(models.Model):
    USER_ROLE_CHOICES = [('user', 'User'), ('admin', 'Admin')]  # Example choices
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=255, choices=USER_ROLE_CHOICES, default='user')
    phone = PhoneNumberField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} ({self.role})"
