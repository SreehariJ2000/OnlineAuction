# Generated by Django 4.2.5 on 2023-11-05 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
