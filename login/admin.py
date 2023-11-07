from django.contrib import admin
from .models import User, Exercise

class UserAdmin (admin.ModelAdmin):
    readonly_fields = ["username","email","todayLoginAttempts","lastLoginAttemptDate","last_login"]
    exclude = ["password"]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Exercise)