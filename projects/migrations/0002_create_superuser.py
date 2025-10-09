# projects/migrations/0002_create_superuser.py
from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ernesto.piura@est.ulsa.edu.ni')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '1234!')  # default temporal

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0001_initial'),  # ajusta esto al último migration file de tu app
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
