# Generated by Django 2.1.5 on 2019-04-01 09:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20190329_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pysakkivalinta',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
