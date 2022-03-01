# Generated by Django 2.1.5 on 2022-02-15 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20220215_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='paymentmode',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.PaymentMode', verbose_name='Mode of Payment'),
            preserve_default=False,
        ),
    ]
