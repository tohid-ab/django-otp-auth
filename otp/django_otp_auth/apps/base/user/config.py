from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "django_otp_auth.apps.base.user"
    verbose_name = _("User")
    #
    # def ready(self):
    #     from . import signals  # noqa
