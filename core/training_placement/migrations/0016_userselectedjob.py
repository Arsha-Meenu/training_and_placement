# Generated by Django 4.2.4 on 2023-09-15 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_placement', '0015_job_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSelectedJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobs', models.ManyToManyField(related_name='selected_jobs', to='training_placement.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
