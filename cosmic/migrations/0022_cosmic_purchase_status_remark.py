# Generated by Django 5.0 on 2024-04-11 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmic', '0021_supplier_profile_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmic_purchase',
            name='status_remark',
            field=models.TextField(blank=True, null=True),
        ),
    ]