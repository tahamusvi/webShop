# Generated by Django 4.2.3 on 2023-08-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0016_color_product_colors'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='more_info',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
