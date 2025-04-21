from django.db import transaction
from .models import CourseCategory

def setup_categories(sender, **kwargs):
    with transaction.atomic():
        categories = [
            {
                'name': 'Special Education and Inclusive Practices',
                'code': 'SEIP',
                'description': 'Courses focusing on inclusive education practices'
            },
            {
                'name': 'Artificial Intelligence',
                'code': 'AI',
                'description': 'Courses on AI technologies and applications'
            },
            {
                'name': 'Classroom Management and Student Engagement',
                'code': 'CMSE',
                'description': 'Courses on effective classroom strategies'
            }
        ]
        
        for category_data in categories:
            CourseCategory.objects.get_or_create(
                code=category_data['code'],
                defaults=category_data
            )