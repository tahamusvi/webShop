# Generated by Django 4.2.3 on 2023-11-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facades', '0031_alter_configshop_home_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='configshop',
            name='news',
            field=models.BooleanField(default=True),
        ),
    ]
