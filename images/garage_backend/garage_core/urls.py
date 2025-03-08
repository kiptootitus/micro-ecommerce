from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('garage/', include('garage.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('cart/', include('cart.urls')),
    path('products/', include('products.urls')),
    # path('orders/', include('orders.urls')),
    # path('vendor/', include('vendor.urls')),
    # path('payment/', include('payment.urls')),
    # path('shipment/', include('shipment.urls')),
]

# Append static & media files handling at the end
if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
