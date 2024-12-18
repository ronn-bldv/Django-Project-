# Generated by Django 5.1.3 on 2024-12-05 11:59

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieDateTime',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='date',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='seat_number',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='time',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='movie_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='seat',
            field=models.CharField(default='Not Assigned', max_length=10),
        ),
        migrations.AlterField(
            model_name='cart',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='moviecategory',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='available_dates',
            field=models.ManyToManyField(related_name='movies', to='home.moviedatetime'),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('seat_number', models.CharField(max_length=10)),
                ('is_taken', models.BooleanField(default=False)),
                ('movie_datetime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='home.moviedatetime')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
