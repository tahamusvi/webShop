# Generated by Django 4.2.3 on 2024-08-30 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='interception_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]