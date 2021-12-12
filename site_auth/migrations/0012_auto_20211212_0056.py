# Generated by Django 3.2.9 on 2021-12-12 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_auth', '0011_alter_smscode_expiration_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smscode',
            name='expiration_date',
        ),
        migrations.AddField(
            model_name='smscode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
