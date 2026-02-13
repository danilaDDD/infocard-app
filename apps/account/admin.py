from django.contrib import admin

from apps.account.models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'phone', 'email', 'is_active', )
    readonly_fields = ('created', 'updated', )
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'patronymic', 'email',
                                         'phone', 'birth_date', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Dop', {'fields': ('created', 'updated', )}),
    )