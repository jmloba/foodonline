# Generated by Django 5.0.3 on 2024-03-23 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testarea', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicemaster',
            name='invoice_desc',
            field=models.CharField(max_length=100),
        ),
    ]
