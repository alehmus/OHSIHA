# Generated by Django 2.1.5 on 2019-03-29 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_profile_pysakkivalinta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pysakkivalinta',
            field=models.IntegerField(default=0),
        ),
    ]
