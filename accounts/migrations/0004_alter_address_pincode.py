# Generated by Django 3.2.5 on 2021-08-01 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.IntegerField(),
        ),
    ]
