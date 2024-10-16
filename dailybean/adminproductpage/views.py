from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from home.models import Product, Review
from .forms import AddProductForm, ModifyProductForm

# Create your views here.

def view_products(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
    }
    return render(request, 'admin/product_page.html', context)

@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminproductpage')
    else:
        form = AddProductForm()
    context = {
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
        'form': form,
    }
    return render(request, 'admin/add_product.html', context)

@user_passes_test(lambda u: u.is_staff)
def modify_product(request, pk):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ModifyProductForm(request.POST)
        if form.is_valid():
            # NEED PK
            # product_id = request.POST.get('product_id')
            product_name = request.POST.get('name')
            product = products.objects.get(name=product_name)
            product.name = form.cleaned_data['changed_name']
            product.imageurl = form.cleaned_data['changed_imageurl']
            product.description = form.cleaned_data['changed_description']
            product.save()
            return redirect('adminproductpage')
    else:
        form = ModifyProductForm()
    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
        'form': form,
    }
    # product = get_object_or_404(Product, pk=pk)
    return render(request, 'admin/product_page.html', context)
   

def view_product_reviews(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    return render(request, 'admin/modify_product.html', {'product': product, 'reviews': reviews})

