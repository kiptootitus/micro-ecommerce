from django.contrib import admin

from accounts.models import Address, Contact, Profile

# Register your models here.
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Profile)
