from django.core.exceptions import ValidationError


class OneLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir une lettre", code="one_letter_error"
            )

    def get_help_text(self):
        return "Le mot de passe doit contenir au moins une lettre"


class OneDigitValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir un chiffre", code="one_digit_error"
            )

    def get_help_text(self):
        return "Le mot de passe doit contenir au moins un chiffre"
