# Generated by Django 5.0 on 2024-07-29 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cosmic', '0034_grn_grnitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='grn',
            new_name='cosmic_grn',
        ),
        migrations.RenameModel(
            old_name='grnitem',
            new_name='cosmic_grnitem',
        ),
    ]