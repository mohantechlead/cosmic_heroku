# Generated by Django 5.0 on 2024-07-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmic', '0035_rename_grn_cosmic_grn_rename_grnitem_cosmic_grnitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmic_grn',
            name='total_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
