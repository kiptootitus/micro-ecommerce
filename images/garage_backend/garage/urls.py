from django.urls import path
from .views import home, category_products, product_detail

urlpatterns = [
    path('', home, name='home'),
    path('category/<str:category>/', category_products, name='category_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
