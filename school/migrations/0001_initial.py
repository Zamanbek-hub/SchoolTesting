# Generated by Django 3.0.6 on 2020-06-17 16:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.PositiveIntegerField()),
                ('id_answer', models.PositiveIntegerField()),
                ('answer', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField()),
                ('duration', models.DurationField(blank=True, default=datetime.timedelta(0))),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(blank=True, max_length=40, verbose_name='school')),
                ('phone', models.CharField(blank=True, max_length=16, verbose_name='phone')),
                ('result', models.CharField(blank=True, max_length=4, verbose_name='result')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Grade')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.PositiveIntegerField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Testing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Subject')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Variant')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ImageField(blank=True, upload_to='questions')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Variant')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
            ],
        ),
    ]
