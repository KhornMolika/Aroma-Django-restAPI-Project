# Generated by Django 5.2.2 on 2025-07-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_created_at_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='full_name',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_proof',
            field=models.ImageField(blank=True, null=True, upload_to='images/PaymentProof/'),
        ),
    ]
