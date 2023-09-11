# Generated by Django 4.2.3 on 2023-09-11 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0021_alter_product_rating'),
        ('blog', '0002_alter_category_options_alter_post_options'),
        ('accounts', '0029_alter_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='product',
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            bases=('accounts.comment',),
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.comment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='stuff.product')),
            ],
            bases=('accounts.comment',),
        ),
    ]
