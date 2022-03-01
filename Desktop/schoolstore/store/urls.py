from django.urls import path
from store import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'store'

urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('home', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('printform/<int:id>/', views.printform, name='printform'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    url(r'^search/$', views.searchposts, name='searchposts'),
    url(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^shop_single(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.shop_single, name='shop_single'),
    path('add-record/', views.add_record, name='add_record'),
    path('print-reciept/<int:id>/', views.printform, name='printform'),
    path('add-category/', views.add_category, name='add_category'),
    path('ajax/load-class/', views.load_class, name='ajax_load_class'),
    path('ajax/load-classarm/', views.load_classarm, name='ajax_load_classarm'),
    path('ajax/load-gender/', views.load_gender, name='ajax_load_gender'),
    path('ajax/load-programtype/', views.load_programtype,
         name='ajax_load_programtype'),
    # path('my-profile/', views.my_profile, name='my_profile'),
    # path('edit-form/', views.edit_form, name='edit_form'),
    # path('pass-form/', views.pass_form, name='pass_form'),
    path('list-post/', views.ListPost.as_view(), name='list_post'),
    path('transactions/', views.transaction, name='transaction'),
    path('category-list/', views.CategoryList.as_view(), name='category_list'),
    path('user-list/', views.UserListPost.as_view(), name='user_list'),
    # path('detail-post/<int:pk>', views.DetailPost.as_view(), name='detail_post'),
    # path('login_page/', auth_views.LoginView.as_view(template_name='backend/login.html'), name='login'),
    # path('logout-page/', auth_views.LogoutView.as_view(
    #     template_name='backend/logout.html'), name='logout'),
]
