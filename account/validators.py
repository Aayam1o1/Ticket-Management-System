"""
Custom Validators.

This module contains custom validators for Django models and forms.

"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number


def validate_phone_number(phone, country=None):
    """
    Validate that the phone number value is valid or not.

    Args:
        phone (string): value to be validated.
        country (any): region for the passed phone number.

    Raises:
        ValidationError: error with msg.

    """
    from account.enums import AccountErrorCode

    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.", code=AccountErrorCode.INVALID
        )
    return phone_number
