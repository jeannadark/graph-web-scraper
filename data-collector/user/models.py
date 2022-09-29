from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from .validators import CustomEmailValidator


class CustomUser(AbstractUser):

    username = None

    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[CustomEmailValidator],
        help_text=_('Emails ending with ada.edu.az are only accepted.'),
        error_messages={
            'unique': _("An user with that email already exists."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
