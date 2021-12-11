from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SMSCode

admin.site.register(User, UserAdmin)
admin.site.register(SMSCode)
