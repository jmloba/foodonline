# Generated by Django 5.0.3 on 2024-03-24 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_alter_openinghour_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]
