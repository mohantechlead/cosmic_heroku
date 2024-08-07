# Generated by Django 5.0 on 2024-06-10 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmic', '0025_cosmic_income_amount_cosmic_income_details_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='cosmic_expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.TextField(null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField(blank=True, null=True)),
                ('purpose', models.TextField(blank=True, null=True)),
                ('reference', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
