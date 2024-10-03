from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_modified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_modified', 'user_type')
    readonly_fields = ('user_modified', 'date_joined')

admin.site.register(User, UserAdmin)