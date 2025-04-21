from django.core.exceptions import ValidationError

from educare.courses import models


def validate_percentage(value):
    if value < 0 or value > 100:
        raise ValidationError('Percentage must be between 0 and 100')

progress_percentage = models.IntegerField(validators=[validate_percentage])    
