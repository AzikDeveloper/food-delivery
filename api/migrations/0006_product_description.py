# Generated by Django 3.2.9 on 2021-12-06 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=300, null=True),
        ),
    ]