# Generated by Django 5.0 on 2024-04-01 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmic', '0017_invoice_item_invoice_num_item_codes_new_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping_info',
            name='container_no',
            field=models.TextField(blank=True, null=True),
        ),
    ]
