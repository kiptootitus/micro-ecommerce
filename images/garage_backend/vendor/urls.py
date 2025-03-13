from django.urls import path
from .views import RegisterVendorView, LoginVendorView, VendorListView, VendorDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('register/', RegisterVendorView.as_view(), name='register_vendor'),
    path('login/', LoginVendorView.as_view(), name='login_vendor'),
    path('vendors/', VendorListView.as_view(), name='vendors'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
