import random, string, uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone


class OTPCodeQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, code):
        time_c = timezone.now()
        return self.filter(
            receiver=receiver,
            uuid=request,
            code=code,
            used=False,
            created__lte=time_c,
            created__gte=time_c-timedelta(seconds=120),
        ).exists()


def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=5)
    return ''.join(digits)


class OTPManager(models.Manager):

    def get_queryset(self):
        return OTPCodeQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)

    def generate(self, data):
        otp = self.model(receiver=data['receiver'])
        otp.save(using=self._db)
        return otp


class OTPCode(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='UUID')
    receiver = models.CharField(max_length=12, verbose_name='mobile number',)
    code = models.CharField(max_length=5, default=generate_otp, verbose_name='OTP code')
    used = models.BooleanField(default=False, verbose_name='USED')
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()

    class Meta:
        ordering = ['-created']
        verbose_name = 'User OTP Code'
        verbose_name_plural = 'User OTP Code'