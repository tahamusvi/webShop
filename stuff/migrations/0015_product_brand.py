# Generated by Django 4.2.3 on 2023-08-14 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0014_rename_images_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='stuff.brand'),
            preserve_default=False,
        ),
    ]