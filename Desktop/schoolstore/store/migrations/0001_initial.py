# Generated by Django 2.1.5 on 2022-01-31 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_category', models.CharField(db_index=True, max_length=150, verbose_name='Item Category')),
                ('item_quantity', models.PositiveIntegerField()),
                ('unique_name', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('item_category',),
            },
        ),
        migrations.CreateModel(
            name='ClassArm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_arm', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.FileField(upload_to='images', verbose_name='Upload Proof of Payment')),
                ('outstanding', models.CharField(max_length=500, verbose_name='Outstanding')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False, verbose_name='Tick to proceed')),
                ('packaged', models.BooleanField(default=False, verbose_name='Tick only if packaged')),
                ('disburse', models.BooleanField(default=False, verbose_name='Tick only if disbursed')),
                ('item_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Category', verbose_name='items')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Gender', verbose_name='Gender')),
            ],
            options={
                'verbose_name': 'inventory',
                'verbose_name_plural': 'inventory',
                'ordering': ('upload_date',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product_price1', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_type', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name1', models.CharField(max_length=100, verbose_name='item name')),
                ('product_price1', models.FloatField(verbose_name='amount')),
                ('slug', models.SlugField(max_length=1000)),
                ('available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopproduct', to='store.Category')),
            ],
            options={
                'ordering': ('product_name1',),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentclass', models.CharField(max_length=30)),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Gender', verbose_name='gender')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(db_index=True, max_length=100, verbose_name='Student Name')),
                ('student_gender', models.CharField(blank=True, max_length=500, verbose_name='Gender')),
                ('slug', models.SlugField(unique=True)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('student_name',),
            },
        ),
        migrations.AlterIndexTogether(
            name='studentrecord',
            index_together={('id', 'slug')},
        ),
        migrations.AddField(
            model_name='studentclass',
            name='studentrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StudentRecord', verbose_name='studentrecord'),
        ),
        migrations.AddField(
            model_name='programtype',
            name='studentrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StudentRecord', verbose_name='studentrecord'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.ShopProduct'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Size'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='studentclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StudentClass', verbose_name='Class'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='studentrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StudentRecord', verbose_name='Full name'),
        ),
        migrations.AddField(
            model_name='gender',
            name='studentrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StudentRecord', verbose_name='studentrecord'),
        ),
        migrations.AddField(
            model_name='classarm',
            name='studentrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StudentRecord', verbose_name='studentrecord'),
        ),
        migrations.AlterIndexTogether(
            name='shopproduct',
            index_together={('id', 'slug')},
        ),
    ]