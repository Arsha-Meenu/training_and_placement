# Generated by Django 4.2.4 on 2023-09-15 05:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_placement', '0012_remove_job_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
