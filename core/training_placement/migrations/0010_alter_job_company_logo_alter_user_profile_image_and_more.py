# Generated by Django 4.2.4 on 2023-09-14 17:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_placement', '0009_alter_user_profile_image_alter_user_upload_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company_logo',
            field=models.FileField(null=True, upload_to='company_logo', validators=[django.core.validators.FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png', 'webp', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip', 'avif'])], verbose_name='company logo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='profile-images', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='user',
            name='upload_resume',
            field=models.FileField(blank=True, null=True, upload_to='uploaded-resume', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'mp3', 'aac', 'm4a', 'mp4', 'ogg', 'odt'])]),
        ),
    ]
