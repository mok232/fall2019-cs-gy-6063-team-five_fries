# Generated by Django 2.2.7 on 2019-11-12 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0007_auto_20191112_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='estimated_rent_price_currency',
            field=models.CharField(blank=True, default='USD', max_length=10, null=True),
        ),
    ]