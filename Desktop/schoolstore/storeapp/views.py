import datetime
from django.shortcuts import render, redirect, get_object_or_404
from storeapp.forms import *
from django.views.decorators.http import require_POST
from django.contrib import messages
# from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from store.models import Inventory, Category
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from store.cart import Cart
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser == True:
                login(request, user)
                return redirect('storeapp:index')
            else:
                messages.error(request, 'Invalid User')
                return render(request, 'storeapp/login.html')
        else:
            messages.error(request, 'Access Denied')
    return render(request, 'storeapp/login.html')


@login_required(login_url='/storeapp/')
def home(request):
    object_overall = Inventory.objects.all().exclude(
        packaged=True).exclude(disburse=True)
    list_object = Inventory.objects.filter(disburse=True)
    object_list = Inventory.objects.all().exclude(
        packaged=True).exclude(disburse=True)
    package_list = Inventory.objects.filter(
        packaged=True).exclude(disburse=True)

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            qs = Inventory.objects.filter(
                upload_date__range=[start_date, end_date])
            return render(request, 'storeapp/filter.html', {'qs': qs, 'form': form})
    else:
        form = DateRangeForm()
    if request.method == 'POST':
        add_form = PackagedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()
            messages.success(
                request, 'Item is now available for disbursal')
    else:
        add_form = PackagedForm()
    if request.method == 'POST':
        add_form = DisbursedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()
    else:
        add_form = DisbursedForm
    context = {
        'object_list': object_list,
        'package_list': package_list,
        'list_object': list_object,
        'object_overall': object_overall,
        'form': form,
    }
    return render(request, 'storeapp/home.html', context)


@login_required(login_url='/storeapp/')
def logout_user(request):
    logout(request)
    return redirect('storeapp:login_view')


@login_required(login_url='/storeapp/')
def change_password(request):
    if request.method == 'POST':
        change_password = ChangePasswordForm(
            data=request.POST, user=request.user)
        if change_password.is_valid():
            change_password.save()
            update_session_auth_hash(request, change_password.user)
            messages.success(request, 'Password Changed Successfully')
    else:
        change_password = ChangePasswordForm(user=request.user)
    return render(request, 'storeapp/change-password.html', {'change_pass': change_password})


@login_required
def store_dashboard(request, item_categoryname_id=None):
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    # object_list = Inventory.objects.order_by('-upload_date')
    object_list = Inventory.objects.filter(
        active=True).exclude(packaged=True)
    paginator = Paginator(object_list, 20)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        list = paginator.page(paginator.num_pages)
    if item_categoryname_id:
        category = get_object_or_404(ShopProduct, id=item_categoryname_id)
        list = Inventory.objects.filter(
            item_categoryname=category).exclude(packaged=True)
    if request.method == 'POST':
        add_form = PackagedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()
            messages.success(
                request, 'Item is now available for disbursal')
    else:
        add_form = PackagedForm()

    context = {
        'list': list,
        'category': category,
        'categories': categories,
        'object_list': object_list,
        'cart': cart,
        # 'order': order,
        'add_form': add_form,
    }
    return render(request, 'storeapp/index.html', context)


@require_POST
def package_submit(request, id):
    package = Inventory.objects.get(id=id)
    package.packaged = True
    package.save()
    return redirect('storeapp:store_dashboard')


@require_POST
def disburse_submit(request, id):
    disbursed = Inventory.objects.get(id=id)
    disbursed.disburse = True
    disbursed.save()
    return redirect('storeapp:packaged')


@login_required(login_url='/storeapp/')
def searchposts(request):
    if request.method == 'POST':
        add_form = PackagedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()
            messages.success(
                request, 'Item is now available for disbursal')
    else:
        add_form = PackagedForm()
    if request.method == 'POST':
        add_form = DisbursedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()

    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(id__icontains=query)

            results = Inventory.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton, 'add_form': add_form}

            return render(request, 'storeapp/search.html', context)

        else:
            return render(request, 'storeapp/index.html')

    else:
        return render(request, 'storeapp/index.html')


def packaged(request):
    object_list = Inventory.objects.filter(
        packaged=True).exclude(disburse=True)
    list_object = Inventory.objects.filter(disburse=True)
    if request.method == 'POST':
        add_form = DisbursedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()
            context = {
                'list_object': list_object,
                'add_form': add_form,
                'object_list': object_list,
            }
            return render(
                request, 'store/disbursed', context)
    else:
        add_form = DisbursedForm()
    return render(request, 'storeapp/packaged.html', {'add_form': add_form, 'object_list': object_list})


def disburse(request):
    list_object = Inventory.objects.filter(disburse=True)
    if request.method == 'POST':
        add_form = DisbursedForm(request.POST)
        if add_form.is_valid():
            add = add_form.save(commit=False)
            add.save()
            context = {
                'list_object': list_object,
                'add_form': add_form,
            }
            messages.success(
                request, 'Item has been disbursed successfully', context)
    else:
        add_form = DisbursedForm()
    return render(request, 'storeapp/disbursed.html', {'add_form': add_form, 'list_object': list_object})
