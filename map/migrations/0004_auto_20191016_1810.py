# Generated by Django 2.2.6 on 2019-10-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_auto_20191015_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citystreetspot',
            name='picture',
            field=models.ImageField(upload_to='./map/static/map'),
        ),
    ]
