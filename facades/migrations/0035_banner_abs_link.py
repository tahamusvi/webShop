# Generated by Django 4.2.3 on 2024-02-03 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facades', '0034_configshop_e_namad'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='abs_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
