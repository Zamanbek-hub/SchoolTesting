# Generated by Django 3.0.6 on 2020-06-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='parents_phone',
            field=models.CharField(blank=True, max_length=16, verbose_name='parents_phone'),
        ),
    ]