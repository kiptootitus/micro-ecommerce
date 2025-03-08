from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    # Extract unique categories and group products by category
    categories = set(products.values_list('category', flat=True))
    categorized_products = {category: products.filter(category=category) for category in categories}

    return render(request, 'ecommerce/home.html', {
        'products': products,
        'categories': categories,  # Pass unique categories
        'categorized_products': categorized_products,  # Dictionary for grouped products
        'query': query
    })

def category_products(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'ecommerce/category_products.html', {
        'category': category,
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ecommerce/product_detail.html', {'product': product})
