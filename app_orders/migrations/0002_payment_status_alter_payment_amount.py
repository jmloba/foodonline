# Generated by Django 5.0.4 on 2024-06-17 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.CharField(max_length=10),
        ),
    ]
