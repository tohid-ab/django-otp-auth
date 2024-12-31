from django.utils.translation import gettext_lazy as _


class GenderType:
    UNKNOWN = 'unknown'
    MALE = 'male'
    FEMALE = 'female'

    CHOICES = [
        (
            UNKNOWN, _('unknown')
        ),
        (
            MALE, _('Male')
        ),
        (
            FEMALE, _('FeMale')
        ),
    ]
