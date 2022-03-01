from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponse
import datetime
import csv
from django.contrib import admin
from .models import *

admin.site.site_header = 'Ambassadors Store Management System'


# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment;'\
#         'filename={}.csv'.format(opts.verbose_name)
#     writer = csv.writer(response)
#     fields = [field for field in opts.get_fields() if not field.many_to_many
#               and not field.one_to_many]
#     # Write a first row with header information
#     writer.writerow([field.verbose_name for field in fields])
#     # Write data rows
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime('%d/%m/%Y')
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response


# export_to_csv.short_description = 'Export to CSV'

# def order_pdf(obj):
#     return mark_safe('<a href="{}">PDF</a>'.format(
#         reverse('admin_order_pdf', args=[obj.id])))
# order_pdf.short_description = 'Invoice'


# def order_detail(obj):
#     return mark_safe('<a href="{}">View</a>'.format(
#         reverse('admin_order_detail', args=[obj.id])))


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
#                     'updated', order_detail]
#     list_filter = ['paid', 'created', 'updated']
#     inlines = [OrderItemInline]
#     actions = [export_to_csv]


# admin.site.register(Order, OrderAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['item_categoryname', 'unique_name']
    prepopulated_fields = {'unique_name': ('item_categoryname',)}


admin.site.register(Category, CategoryAdmin)


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many
              and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('admin_order_detail', args=[obj.id])))


admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


# admin.site.register(OrderItem)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['studentrecord', 'studentclass', 'sex', 'parenttel', 'size', 'paymentmode', 'account',
                    'upload_date', 'active', 'packaged', 'disburse', order_detail]
    list_filter = ['size', 'studentclass', 'active',
                   'packaged', 'disburse', 'upload_date']
    search_fields = ('studentrecord', 'studentclass')
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Inventory, InventoryAdmin)

admin.site.register(PaymentMode)
admin.site.register(Account)


class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'available', 'slug']
    list_filter = ['student_name',
                   'available']
    search_fields = ('student_name', 'available')
    prepopulated_fields = {'slug': ('student_name',)}


admin.site.register(StudentRecord, StudentRecordAdmin)


class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['studentclass', 'sex']
# list_filter = ['student_name', 'student_class', 'student_gender',
#                'available']
# search_fields = ('student_name', 'student_class', 'student_gender')
# prepopulated_fields = {'slug': ('student_name',)}


admin.site.register(StudentClass, StudentClassAdmin)


class ClassArmAdmin(admin.ModelAdmin):
    list_display = ['studentrecord', 'class_arm']


admin.site.register(ClassArm, ClassArmAdmin)


class GenderAdmin(admin.ModelAdmin):
    list_display = ['studentrecord', 'sex']


admin.site.register(Gender, GenderAdmin)


class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ['studentrecord', 'program_type']


admin.site.register(ProgramType, ProgramTypeAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']


admin.site.register(Size, SizeAdmin)


# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'student_class', 'sex', 'size',
#                     'item_category', 'upload_date', 'quantity')
#     list_filter = ('active', 'created_on')
#     search_fields = ('name', 'email', 'body')
#     actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)


# admin.site.register(Comment, CommentAdmin)
admin.site.register(ShopProduct)
