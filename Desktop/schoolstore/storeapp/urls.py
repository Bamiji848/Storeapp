from django.urls import path
from django.conf.urls import url
from storeapp import views
from django.contrib.auth import views as auth_views

app_name = 'storeapp'

urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('home/', views.home, name="index"),
    url(r'^search/$', views.searchposts, name='searchposts'),
    path('logout-page/', views.logout_user, name='logout_user'),
    path('change-password/', views.change_password, name='change_password'),
    path('store-dashboard/', views.store_dashboard, name="store_dashboard"),
    url(r'^search/$', views.searchposts, name='searchposts'),
    path('packaged-item/', views.packaged, name='packaged'),
    path('disbursed/', views.disburse, name='disburse'),
    url(r'^(?P<product_name1>)/$',
        views.store_dashboard, name='product_list_by_category'),
    path('packaged/<int:id>/', views.package_submit, name='package_submit'),
    path('disbursed/<int:id>/', views.disburse_submit, name='disburse_submit'),
    # url(r'^/(?P<sex_id>[-\w]+)/$',
    #     views.index, name='product_list_by_gender'),
    # path('register/', views.register, name='register'),
    # path('logoutpage/', views.logoutpage, name='logoutpage'),
    # path('my-profile/', views.my_profile, name='my_profile'),
    # path('edit-form/', views.edit_form, name='edit_form'),
    # path('pass-form/', views.pass_form, name='pass_form'),
    # path('list-post/', views.ListPost.as_view(), name='list_post'),
    # path('category-list/', views.CategoryList.as_view(), name='category_list'),
    # path('user-list/', views.UserListPost.as_view(), name='user_list'),
    # path('detail-post/<int:pk>', views.DetailPost.as_view(), name='detail_post'),
    # path('login_page/', auth_views.LoginView.as_view(template_name='backend/login.html'), name='login'),
    # path('logout-page/', auth_views.LogoutView.as_view(
    #     template_name='backend/logout.html'), name='logout'),
]
