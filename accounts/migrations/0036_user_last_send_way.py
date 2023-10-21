# Generated by Django 4.2.3 on 2023-10-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_alter_profileuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_send_way',
            field=models.CharField(choices=[('c', 'درون شهری'), ('b', 'اتوبوس'), ('p', 'پست معمولی')], default=2, max_length=1),
            preserve_default=False,
        ),
    ]