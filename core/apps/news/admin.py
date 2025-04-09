from django.contrib import admin

from core.apps.news.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'middle_name', 'email', 'score', 'created_at', 'updated_at']
    list_display_links = ['id', 'last_name', 'first_name', 'middle_name', 'email']
    list_filter = ['role', 'created_at', 'updated_at']
    search_fields = ['id', 'last_name', 'first_name', 'middle_name', 'email']

