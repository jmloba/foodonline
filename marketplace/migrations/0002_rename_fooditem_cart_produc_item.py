# Generated by Django 5.0.3 on 2024-03-16 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='fooditem',
            new_name='produc_item',
        ),
    ]
