# Generated by Django 3.2.12 on 2023-05-26 03:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsapp', '0019_remove_news_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='voted_comment',
            field=models.ManyToManyField(blank=True, related_name='voted_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
