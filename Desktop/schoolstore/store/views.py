from dis import dis
from email import message
from itertools import product
import mimetypes
from urllib import response
from django.shortcuts import get_object_or_404, render, redirect

from storeapp.views import disburse
from .forms import *
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from store.models import *
from storeapp.forms import *
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from store.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from storeapp.forms import PackagedForm, DisbursedForm
from django.db.models import Sum, F, FloatField, ExpressionWrapper
import csv


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff == True:
                login(request, user)
                return redirect('store:index')
            else:
                messages.error(request, 'Invalid User')
                return render(request, 'store/login.html')
        else:
            messages.error(request, 'Access Denied')
    return render(request, 'store/login.html')


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Inventory, id=order_id)
    return render(request, 'admin/detail.html', {'order': order})


@login_required(login_url='/store/')
def index(request):
    object_list = Inventory.objects.all().exclude(disburse=True)
    inventory = Inventory.objects.all()
    context = {
        'object_list': object_list,
        'inventory': inventory,
    }
    return render(request, 'store/index.html', context)


@login_required(login_url='/store/')
def register(request):
    if request.method == 'POST':
        register_form = Register(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(
                request, 'User have been added successfully')
    else:
        register_form = Register()
    return render(request, 'store/add-user.html', {'register_form': register_form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('store:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')


@login_required(login_url='/store/')
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})
    if request.method == 'POST':
        add_form = InventoryForm(request.POST)
        if add_form.is_valid():
            studentrecord = add_form.cleaned_data['studentrecord']
            studentclass = add_form.cleaned_data['studentclass']
            sex = add_form.cleaned_data['sex']
            size = add_form.cleaned_data['size']
            order = add_form.save(commit=False)
            order = add_form.save()
            inventory = Inventory.objects.get(id=order.id)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 'update': True})
            inventory = Inventory.objects.get(id=order.id)
            item = OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_price1=item['product_price1'],
                quantity=item['quantity']
            )
        cart.clear()
        context = {
            'studentrecord': studentrecord,
            'studentclass': studentclass,
            'sex': sex,
            'size': size,
            'order': order,
            'item': item,
            'cart': cart,
            'add_form': add_form,
            'inventory': inventory,
        }
        # messages.success(
        #     request, 'Item has been ordered successfully', context)
        # return render(request, 'store/print-form.html', context)
        return redirect('store:list_post')
    else:
        add_form = InventoryForm()
    return render(request, 'store/cart.html', {'cart': cart, 'add_form': add_form})


def printform(request, id):
    try:
        inventory = get_object_or_404(Inventory, id=id)
    except Inventory.DoesNotExist:
        Http404('The page you are accessing does not exist')
    return render(request, 'store/print-form.html', {'inventory': inventory})


@login_required(login_url='/store/')
def shop(request, category_slug=None):
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    products = ShopProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = ShopProduct.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'cart': cart
    }
    return render(request, 'store/shop.html', context)


@login_required(login_url='/store/')
def shop_single(request, id, slug, category_slug=None):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    products = ShopProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = ShopProduct.objects.filter(category=category)

    context = {
        'product': product,
        'products': products,
        'cart_product_form': cart_product_form,
        'cart': cart
    }
    return render(request, 'store/shop-single.html', context)


@login_required(login_url='/store/')
def add_record(request):
    cart = Cart(request)
    if request.method == 'POST':
        add_form = InventoryForm(request.POST, request.FILES)
        if add_form.is_valid():
            studentrecord = add_form.cleaned_data['studentrecord']
            studentclass = add_form.cleaned_data['studentclass']
            sex = add_form.cleaned_data['sex']
            size = add_form.cleaned_data['size']
            # receipt = add_form.cleaned_data['receipt']
            outstanding = add_form.cleaned_data['outstanding']
            # item_category = add_form.cleaned_data['item_category']
            quantity = add_form.cleaned_data['quantity']
            add = add_form.save(commit=False)
            add.save()
            # new_id = add.id
            # add_form.save_m2m()
            context = {
                'studentrecord': studentrecord,
                'studentclass': studentclass,
                'sex': sex,
                'size': size,
                # 'receipt': receipt,
                'outstanding': outstanding,
                # 'item_category': item_category,
                'quantity': quantity,
                'new_id': new_id,
            }
            messages.success(
                request, 'Item has been ordered successfully', context)
            # return render(request, 'store/print-form.html', context)
    else:
        add_form = InventoryForm()
    return render(request, 'store/add-record.html', {'add_form': add_form})


@login_required(login_url='/store/')
def searchposts(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(id__icontains=query)

            results = Inventory.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'store/search.html', context)

        else:
            return render(request, 'store/index.html')

    else:
        return render(request, 'store/index.html')


def load_class(request):
    studentrecord_id = request.GET.get('studentrecord')
    studentclass = StudentClass.objects.filter(
        studentrecord_id=studentrecord_id).order_by('studentrecord')
    return render(request, 'store/studentrecord_dropdown.html', {'studentclass': studentclass})


def load_classarm(request):
    studentrecord_id = request.GET.get('studentrecord')
    class_arm = ClassArm.objects.filter(
        studentrecord_id=studentrecord_id).order_by('studentrecord')
    return render(request, 'store/studentrecord_class_arm.html', {'class_arm': class_arm})


def load_gender(request):
    studentrecord_id = request.GET.get('studentrecord')
    sex = Gender.objects.filter(
        studentrecord_id=studentrecord_id).order_by('studentrecord')
    return render(request, 'store/studentrecord_gender.html', {'sex': sex})


def load_programtype(request):
    studentrecord_id = request.GET.get('studentrecord')
    program_type = ProgramType.objects.filter(
        studentrecord_id=studentrecord_id).order_by('studentrecord')
    return render(request, 'store/loadprogram_type.html', {'program_type': program_type})


@login_required(login_url='/store/')
def add_category(request):
    cat = ShopProduct.objects.all()
    if request.method == 'POST':
        cat_form = ShopProductForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(
                request, 'Category added successfully')
    else:
        cat_form = ShopProductForm()
    return render(request, 'store/add-category.html', {'cat_form': cat_form, 'cat': cat})


@login_required(login_url='/store/')
def logoutpage(request):
    logout(request)
    return redirect('store:index')


class ListPost(ListView):
    model = Inventory
    queryset = Inventory.objects.order_by('-upload_date')
    template_name = 'store/list-post.html'
    paginate_by = 20


class UserListPost(ListView):
    model = User
    template_name = 'store/user-list.html'
    context_object_name = 'user_list'


class CategoryList(ListView):
    model = Category
    template_name = 'store/category-list.html'
    context_object_name = 'category_list'


def transaction(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            object_list = OrderItem.objects.filter(
                created__range=[start_date, end_date])
            object_list1 = OrderItem.objects.filter(created__range=[start_date, end_date]).values('product').annotate(price_sum=ExpressionWrapper(
                Sum(F('quantity') * F('product__product_price1')), output_field=FloatField()),
                quantity_sum=Sum('quantity'),
                product_name=F('product__product_name1')
            )
            total_amount = sum(object_list1.values_list(
                'price_sum', flat=True))
            total_quantity = sum(object_list.values_list(
                'quantity', flat=True))
            context = {
                'object_list1': object_list1,
                'form': form,
                'total_quantity': total_quantity,
                'total_amount': total_amount,
                'start_date': start_date,
                'end_date': end_date
            }
            return render(request, 'store/transaction.html', context)
    else:
        form = DateRangeForm()
    return render(request, 'store/transaction.html', {'form': form})
