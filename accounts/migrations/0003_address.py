# Generated by Django 3.2.5 on 2021-08-01 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=14)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pincode', models.IntegerField(max_length=10)),
                ('address_type', models.CharField(max_length=10)),
                ('default', models.BooleanField(default=False)),
                ('address_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
