# Generated by Django 5.1.2 on 2024-10-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dutyroster',
            name='shift_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dutyroster',
            name='shift_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='education',
            field=models.CharField(blank=True, choices=[('12th', '12th'), ('UG', 'UG'), ('SSLC', 'SSLC'), ('PG', 'PG')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, null=True),
        ),
    ]
