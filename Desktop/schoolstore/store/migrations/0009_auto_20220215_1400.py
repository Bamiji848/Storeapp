# Generated by Django 2.1.5 on 2022-02-15 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20220215_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.Account', verbose_name='Which Account did parent transfer To'),
            preserve_default=False,
        ),
    ]