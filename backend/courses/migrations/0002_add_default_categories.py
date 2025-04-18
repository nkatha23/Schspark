from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('courses', 'CourseCategory')
    Category.objects.bulk_create([
        Category(name='STEM', code='STEM', description='Science, Technology, Engineering, Math'),
        Category(name='Art', code='ART', description='Creative Arts'),
        Category(name='AI', code='AI', description='Artificial Intelligence'),
    ])

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0001_initial'),  # Make sure this matches your last migration
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]