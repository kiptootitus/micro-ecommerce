from django.contrib import admin

from accounts.models import Address, Contact, Profile, User

# Register your models here.
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Profile)
