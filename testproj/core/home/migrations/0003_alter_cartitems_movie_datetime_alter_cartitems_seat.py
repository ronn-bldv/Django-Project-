# Generated by Django 5.1.3 on 2024-12-05 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_moviedatetime_remove_cartitems_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='movie_datetime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.moviedatetime'),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.seat'),
        ),
    ]
