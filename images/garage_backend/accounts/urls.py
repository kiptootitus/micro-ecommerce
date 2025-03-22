from django.urls import path, include

from .views import (UserListCreateView, UserDetailView,
                    CustomSignupView, CustomLoginView, CustomLogoutView)

urlpatterns = [
    # API endpoints
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Allauth endpoints with custom views
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
]
