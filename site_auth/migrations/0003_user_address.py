# Generated by Django 3.2.9 on 2021-12-11 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20211210_1526'),
        ('site_auth', '0002_rename_phone_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.address'),
        ),
    ]
