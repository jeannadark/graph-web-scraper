from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomEmailValidator(EmailValidator):
    message = _(
        _('Enter a valid email. This value must end with ada.edu.az ending')
    )
    domain_whitelist = ['ada.edu.az']