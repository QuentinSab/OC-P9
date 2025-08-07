from django.core.exceptions import ValidationError


class OneLetterValidator:
    """
    Ensure the password contains at least one letter (a-z or A-Z).
    """

    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError("Le mot de passe doit contenir une lettre.", code="one_letter_error")

    def get_help_text(self):
        return "Le mot de passe doit contenir au moins une lettre."


class OneDigitValidator:
    """
    Ensure the password contains at least one digit (0-9).
    """

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError("Le mot de passe doit contenir un chiffre.", code="one_digit_error")

    def get_help_text(self):
        return "Le mot de passe doit contenir au moins un chiffre."
