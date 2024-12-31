from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali

User = get_user_model()

UserAdmin.fieldsets += (_('Info Account'), {'fields': (
                        'mobile_number',
                        'gender',
                        'birthday',
                        )}),


class MyUserAdmin(UserAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'mobile_number',
        'get_date_joined_jalali'
    ]

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'mobile_number'
    )

    list_display_links = ('username',)

    def get_date_joined_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%Y/%m/%d - %H:%M:%S')

    get_date_joined_jalali.short_description = 'Date Joined'


admin.site.site_header = _("OTP administration")
admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
