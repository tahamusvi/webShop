# Generated by Django 4.2.3 on 2023-11-04 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_bankaccount_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='receipt',
            field=models.ImageField(blank=True, null=True, upload_to='media/receipt/%Y/%m/'),
        ),
    ]
