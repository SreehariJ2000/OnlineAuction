# Generated by Django 4.2.5 on 2024-03-23 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auction_app', '0018_deliveryassignment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryboy',
            name='user',
        ),
        migrations.DeleteModel(
            name='DeliveryAssignment',
        ),
        migrations.DeleteModel(
            name='DeliveryBoy',
        ),
    ]
