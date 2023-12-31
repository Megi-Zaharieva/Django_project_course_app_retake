# Generated by Django 4.2.3 on 2023-08-18 20:33

import base_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0004_createcourse_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createcourse',
            name='video_url',
            field=models.URLField(default=None, validators=[base_app.validators.validate_youtube_url]),
        ),
    ]
