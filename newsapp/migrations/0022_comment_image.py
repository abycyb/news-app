# Generated by Django 3.2.12 on 2023-05-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0021_remove_comment_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.FileField(blank=True, default=None, null=True, upload_to='comment_img'),
        ),
    ]
