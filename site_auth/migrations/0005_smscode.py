# Generated by Django 3.2.9 on 2021-12-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_auth', '0004_alter_user_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, null=True)),
                ('code', models.IntegerField(default=595168, null=True)),
            ],
        ),
    ]
