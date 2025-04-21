from django.apps import AppConfig

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    def ready(self):
        # Use Django's post_migrate signal instead
        from django.db.models.signals import post_migrate
        from .setup import setup_categories
        post_migrate.connect(setup_categories, sender=self)