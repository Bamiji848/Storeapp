# Generated by Django 2.1.5 on 2022-01-31 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20220131_1010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('item_categoryname',), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='item_category',
            new_name='item_categoryname',
        ),
    ]
