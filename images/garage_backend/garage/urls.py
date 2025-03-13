from django.urls import path

from garage.views import TestView

urlpatterns = [
    path('test/', TestView.as_view(), name='test_api_view')
]