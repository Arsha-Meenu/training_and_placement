# Generated by Django 4.2.4 on 2023-09-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_placement', '0019_jobselecteduser_delete_userselectedjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
