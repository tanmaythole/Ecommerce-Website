# Generated by Django 3.2.5 on 2021-08-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0008_auto_20210808_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('paymentSuccess', 'Payment Success'), ('paymentFailed', 'Payment Failed'), ('packed', 'Packed'), ('shipped', 'Shipped'), ('onTheWay', 'On The Way'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ('returned', 'Returned'), ('refunded', 'Refunded')], max_length=256, null=True),
        ),
    ]
