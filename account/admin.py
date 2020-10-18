from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'is_admin', 'is_staff', 'is_active', 'date_joined', 'last_login',)
    # list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'date_joined', 'last_login',)
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active',)}),
        ('Status', {'fields': ('date_joined', 'last_login',)}),
    )

    readonly_fields = ['date_joined', 'last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )

    search_fields = ('email', 'username',)
    ordering = ('username', 'first_name', 'last_name', 'email', 'phone',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)