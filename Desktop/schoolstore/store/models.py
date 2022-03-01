from os import supports_bytes_environ
from django.contrib.admin.options import ModelAdmin
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib import admin
from django.forms import CheckboxSelectMultiple


class Category(models.Model):
    item_categoryname = models.CharField(
        max_length=150, db_index=True, verbose_name='Item Category')
    item_quantity = models.PositiveIntegerField()
    unique_name = models.SlugField(max_length=150, unique=True, db_index=True)

    class Meta:
        ordering = ('item_categoryname', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.item_categoryname


class StudentRecord(models.Model):
    # class = models.ForeignKey(
    #     Category, related_name='shopproduct', on_delete=models.CASCADE)
    student_name = models.CharField(
        max_length=100, verbose_name='Student Name', db_index=True)
    student_gender = models.CharField(
        max_length=500, verbose_name='Gender', blank=True)
    # product_img1 = models.ImageField(
    #     upload_to='images', verbose_name='product1 image')
    # studentclass = models.CharField(
    #     max_length=500, verbose_name='Student Class')
    # product_price = models.CharField(
    #     max_length=200, verbose_name='Item Price', blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('student_name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.student_name


class Gender(models.Model):
    studentrecord = models.ForeignKey(
        StudentRecord, verbose_name='studentrecord', on_delete=models.CASCADE)
    sex = models.CharField(max_length=6)

    def __str__(self):
        return self.sex


class StudentClass(models.Model):
    studentrecord = models.ForeignKey(
        StudentRecord, verbose_name='studentrecord', on_delete=models.CASCADE)
    sex = models.ForeignKey(
        Gender, verbose_name='gender', on_delete=models.CASCADE)
    studentclass = models.CharField(max_length=30)

    def __str__(self):
        return self.studentclass


class ClassArm(models.Model):
    studentrecord = models.ForeignKey(
        StudentRecord, verbose_name='studentrecord', on_delete=models.CASCADE)
    class_arm = models.CharField(max_length=30)

    def __str__(self):
        return self.class_arm


class ProgramType(models.Model):
    studentrecord = models.ForeignKey(
        StudentRecord, verbose_name='studentrecord', on_delete=models.CASCADE)
    program_type = models.CharField(max_length=8)

    def __str__(self):
        return self.program_type


class Size(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return self.size


class MyModelAdmin(admin.ModelAdmin):
    # list_display = ['studentrecord', 'studentclass', 'sex', 'size', 'receipt', 'outstanding',
    #                 'upload_date', 'quantity', 'active']
    list_filter = ['studentrecord', 'sex',
                   'size', 'studentclass', 'active', 'upload_date']
    search_fields = ('studentrecord', 'studentclass', 'outstanding')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    actions = ['approve_orders']

    def approve_orders(self, request, queryset):
        queryset.update(active=True)

        actions = ['approve_orders']

    def approve_orders(self, request, queryset):
        queryset.update(active=True)


class ShopProduct(models.Model):
    # category = models.ForeignKey(
    #     Category, related_name='shopproduct', on_delete=models.CASCADE)
    product_name1 = models.CharField(
        max_length=100, verbose_name='item name')
    # product_content = models.CharField(max_length=500, verbose_name='content')
    # product_img1 = models.ImageField(
    #     upload_to='images', verbose_name='product1 image')
    # product_desc1 = models.CharField(
    #     max_length=100, verbose_name='product1_desc')
    product_price1 = models.FloatField(verbose_name='price')
    slug = models.SlugField(max_length=1000, db_index=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('product_name1', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.product_name1

    def get_absolute_url(self):
        return reverse('store:shop_single', args=[self.id, self.slug])

    def get_absolute_url1(self):
        return reverse('storeapp:product_list_by_category', args=[self.product_name1])


class PaymentMode(models.Model):
    payment = models.CharField(max_length=50)

    def __str__(self):
        return self.payment


class Account(models.Model):
    account = models.CharField(max_length=50)

    def __str__(self):
        return self.account


class Inventory(models.Model):
    studentrecord = models.ForeignKey(
        StudentRecord, verbose_name='Full name', on_delete=models.CASCADE)
    studentclass = models.ForeignKey(
        StudentClass, on_delete=models.CASCADE, verbose_name='Class')
    sex = models.ForeignKey(
        Gender, on_delete=models.CASCADE, verbose_name='Gender')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(
        default=False, verbose_name='Tick to proceed')
    packaged = models.BooleanField(
        default=False, verbose_name='Tick only if packaged')
    disburse = models.BooleanField(
        default=False, verbose_name='Tick only if disbursed')
    paymentmode = models.ForeignKey(
        PaymentMode, on_delete=models.CASCADE, verbose_name='Mode of Payment')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name='Which Account did parent transfer To')
    parenttel = models.CharField(
        max_length=13, verbose_name='Parent Telephone Number(Whatsapp)')

    class Meta:
        ordering = ('upload_date', )
        verbose_name = 'inventory'
        verbose_name_plural = 'inventory'

    def __str__(self):
        return str(self.studentrecord)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # def get_absolute_url(self):
    #     return reverse('store:store_single', args=[self.id, self.slug])

    # def get_absolute_url(self):
    #     return reverse('store:list_post', args=[self.id, self.slug])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Inventory, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product_price1 = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.product.product_price1 * self.quantity
