# Generated by Django 3.2.9 on 2021-12-11 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_auth', '0008_alter_smscode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscode',
            name='code',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
