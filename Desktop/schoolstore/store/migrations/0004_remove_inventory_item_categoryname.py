# Generated by Django 2.1.5 on 2022-01-31 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220131_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='item_categoryname',
        ),
    ]