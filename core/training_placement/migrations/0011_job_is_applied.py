# Generated by Django 4.2.4 on 2023-09-15 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_placement', '0010_alter_job_company_logo_alter_user_profile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_applied',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]