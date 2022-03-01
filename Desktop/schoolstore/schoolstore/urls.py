from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('store/', include('store.urls')),
    path('storeapp/', include('storeapp.urls')),
    path('admin/', admin.site.urls),
    path('admin/order/<int:order_id>/',
         views.admin_order_detail, name='admin_order_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
