# Generated by Django 4.2.3 on 2023-10-19 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0028_remove_product_height_remove_product_length_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='transit_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]