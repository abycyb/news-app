# Generated by Django 3.2.12 on 2023-05-25 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0010_auto_20230525_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='votes',
        ),
    ]