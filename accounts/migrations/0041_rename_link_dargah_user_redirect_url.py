# Generated by Django 4.2.3 on 2024-03-08 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0040_user_link_dargah_user_redirect'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='link_dargah',
            new_name='redirect_url',
        ),
    ]
