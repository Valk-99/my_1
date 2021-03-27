# Generated by Django 3.1.6 on 2021-03-27 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20210327_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_profile',
            field=models.OneToOneField(default='User.username', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
