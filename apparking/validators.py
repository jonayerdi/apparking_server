from django.core.validators import RegexValidator

IsPhoneValidator = RegexValidator(r'^[0-9]{9}$',
                             message='not a valid phone number',
                             code='Invalid Number')