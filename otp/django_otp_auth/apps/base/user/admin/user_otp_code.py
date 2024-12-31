from django.contrib import admin
from jalali_date import datetime2jalali

from django_otp_auth.apps.base.user.models import OTPCode


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "receiver",
        "code",
        "used",
        "get_created_date_jalali"
    ]

    list_display_links = [
        'uuid',
    ]

    list_filter = [
        'created'
    ]

    search_fields = [
        'uuid',
        'receiver'
    ]

    def get_created_date_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%Y/%m/%d - %H:%M:%S')

    get_created_date_jalali.short_description = 'Last Code'
