from django.contrib import admin

from accounts.models import Address, Profile

# Register your models here.
admin.site.register(Address)
admin.site.register(Profile)
