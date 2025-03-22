from django.urls import path

from .views import RegisterVendorView, LoginVendorView, VendorListView, VendorDetailView

urlpatterns = [
    path('register/', RegisterVendorView.as_view(), name='register_vendor'),
    path('login/', LoginVendorView.as_view(), name='login_vendor'),
    path('vendors/<int:pk>', VendorListView.as_view(), name='vendors'),  # Works for class-based views
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
]
