# Generated by Django 4.2.6 on 2023-10-23 21:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instructors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('duration', models.PositiveIntegerField()),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('release_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='instructors.instructor')),
            ],
        ),
    ]
