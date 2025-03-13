from django.urls import path
from . import views

urlpatterns = [
    path('address/', views.AddressListView.as_view(), name='address_list'),
    path('address/<int:pk>/', views.AddressDetailView.as_view(), name='address_detail'),
    path('contact/', views.ContactListView.as_view(), name='contact_list'),
    path('profile/', views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]