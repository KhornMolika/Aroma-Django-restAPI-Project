# Generated by Django 5.2.2 on 2025-07-28 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_product_quantity_alter_blog_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]
