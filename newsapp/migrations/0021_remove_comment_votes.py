# Generated by Django 3.2.12 on 2023-05-26 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0020_comment_voted_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='votes',
        ),
    ]
