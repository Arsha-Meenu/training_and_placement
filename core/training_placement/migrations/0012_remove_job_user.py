# Generated by Django 4.2.4 on 2023-09-15 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_placement', '0011_job_is_applied'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='user',
        ),
    ]
