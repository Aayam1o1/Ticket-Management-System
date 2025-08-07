"""Enum for user models."""

from enum import Enum

class AccountErrorCode(Enum):

    """
        Enum defining error codes related to account authentication and validation.

        Constants:

    INVALID: Indicates a general validation error for the account.
    INVALID_PASSWORD: Indicates an error related to an invalid password.
    INVALID_OTP: Indicates an error related to an invalid One-Time Password (OTP).
    INVALID_CREDENTIALS: Indicates invalid authentication credentials error.

    """

    INVALID = "invalid"
    INVALID_PASSWORD = "invalid_password"
    INVALID_OTP = "invalid_otp"
    INVALID_CREDENTIALS = "invalid_credentials"
