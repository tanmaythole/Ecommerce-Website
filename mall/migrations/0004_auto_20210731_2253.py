# Generated by Django 3.2.5 on 2021-07-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0003_auto_20210731_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='subcat_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
