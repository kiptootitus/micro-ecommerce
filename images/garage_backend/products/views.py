from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user  # Assign the logged-in user as the product owner
            product.save()
            return redirect('home')  # Redirect to homepage or product list after adding
    else:
        form = ProductForm()

    return render(request, 'ecommerce/add_product.html', {'form': form})
