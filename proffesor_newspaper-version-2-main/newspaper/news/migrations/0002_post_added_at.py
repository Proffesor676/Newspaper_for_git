# Generated by Django 4.1.4 on 2023-01-11 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='added_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
