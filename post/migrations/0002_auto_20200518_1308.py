# Generated by Django 3.0.6 on 2020-05-18 07:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 18, 7, 38, 32, 560663, tzinfo=utc)),
        ),
    ]
