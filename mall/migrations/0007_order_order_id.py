# Generated by Django 3.2.5 on 2021-08-07 18:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0006_alter_order_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=25),
            preserve_default=False,
        ),
    ]
