# Generated by Django 3.2.9 on 2021-12-10 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_auth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
