# Generated by Django 4.2.1 on 2023-05-24 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0003_news_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.FileField(blank=True, default=None, null=True, upload_to='media/newsimg'),
        ),
    ]
