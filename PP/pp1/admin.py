from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Paragraph

# Unregister the original Group model from the admin as we're not using it
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'dob', 'is_admin', 'createdAt', 'modifiedAt')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'dob')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Important dates', {'fields': ('last_login', 'createdAt', 'modifiedAt')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'dob', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'createdAt', 'modifiedAt')
    search_fields = ('content', 'user__email')
    list_filter = ('createdAt', 'modifiedAt')
    ordering = ('-createdAt',)

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# and ParagraphAdmin
admin.site.register(Paragraph, ParagraphAdmin)

