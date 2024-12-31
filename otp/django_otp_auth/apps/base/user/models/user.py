from random import choice
from string import ascii_lowercase, digits, ascii_uppercase

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django_otp_auth.settings import USERNAME_START
from django_otp_auth.apps.base.user.enums import GenderType


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, null=True)
    mobile_number = models.CharField(
        verbose_name=_('Mobile Number'),
        max_length=11,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        verbose_name=_('Gender'),
        choices=GenderType.CHOICES,
        default=GenderType.UNKNOWN,
        max_length=10
    )
    birthday = models.DateTimeField(
        verbose_name=_('Birthday'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f'{self.first_name or self.last_name if self.first_name or self.last_name else self.username}  - {self.mobile_number}'

    @classmethod
    def generate_username(cls, length=8, chars=ascii_lowercase + digits + ascii_uppercase):
        username = ''.join([choice(chars) for i in range(length)])
        while cls.objects.filter(username=USERNAME_START + username).exists():
            return cls.generate_username(length=length, chars=chars)
        return USERNAME_START + username

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr) and value is not None:
                setattr(self, attr, value)
        self.save()
