from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_superuser', 'last_login_date', 'created_date')
    search_fields = ('email', 'username')
    readonly_fields = ('created_date', 'last_login_date')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
