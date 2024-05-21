# Generated by Django 5.0.3 on 2024-03-23 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.PositiveIntegerField(unique=True)),
                ('invoice_desc', models.TextField(unique=True)),
                ('invoice_date', models.DateField()),
                ('invoice_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice_image', models.ImageField(upload_to='invoice_image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]