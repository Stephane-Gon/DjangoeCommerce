from django.core.exceptions import ValidationError
import re



class CheckNumberValidator:

    def validate(self, password, user=None):

        if re.search('[0-9]', password) is None:
            raise ValidationError('The password must contain at least one number.')
        
    def get_help_text(self):
        return "The password must contain at least one number."
            


class CheckUpperValidator:

    def validate(self, password, user=None):

        if re.search('[A-Z]', password) is None:
            raise ValidationError('The password must contain at least one upper letter.')
        
    def get_help_text(self):
        return "The password must contain at least one upper letter."

