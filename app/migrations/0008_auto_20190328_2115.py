# Generated by Django 2.1.5 on 2019-03-28 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190327_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='pysakki',
        ),
        migrations.AddField(
            model_name='profile',
            name='pysakki1',
            field=models.CharField(default='Itsenäisyydenkatu 10', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='pysakki2',
            field=models.CharField(default='TTY', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='pysakki3',
            field=models.CharField(default='Ahvenisjärvi', max_length=50),
        ),
    ]
