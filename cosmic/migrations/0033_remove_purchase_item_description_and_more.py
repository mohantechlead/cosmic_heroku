# Generated by Django 5.0 on 2024-07-05 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmic', '0032_cosmic_purchase_conditions_purchase_item_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase_item',
            name='description',
        ),
        # migrations.AddField(
        #     model_name='cosmic_purchase',
        #     name='conditions',
        #     field=models.TextField(blank=True, null=True),
        # ),
    ]