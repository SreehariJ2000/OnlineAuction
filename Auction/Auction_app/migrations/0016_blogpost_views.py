# Generated by Django 4.2.5 on 2024-03-09 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction_app', '0015_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
