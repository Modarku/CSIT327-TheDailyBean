from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from home.models import Product, Review
from .forms import ReviewForm
from payment.models import Order
from django.http import JsonResponse

# Create your views here.

def view_products(request):
    page = request.GET.get('page', 'products')
    template = 'subscriptions.html' if page == 'subscriptions' else 'products.html'

    context = {
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
    }
    return render(request, template, context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=id).order_by('-id')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Set the current user
            review.save()
            return redirect('product_detail', id=id)  # Redirect to the product detail page
        else:
            print("Form errors:", form.errors)
    else:
        form = ReviewForm()

    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'product': get_object_or_404(Product, id=id),
        'reviews': reviews,
        'form' : form,
    }

    return render(request, 'product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    quantity = int(request.POST.get('quantity', 1))

    total_price = product.price * quantity

    Order.objects.create(
        product=product,
        user=user,
        product_amount=quantity,
        total=total_price,
        date_paid=None
    )

    return redirect('product_list')

@csrf_exempt
def delete_review(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'DELETE':
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully.'}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({'message': 'Review not found.'}, status=404)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def edit_review(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id)
    product = get_object_or_404(Product, id=product_id) 
    reviews = Review.objects.filter(product=product_id).order_by('-id')

    if request.method == 'POST':
        form = ReviewForm()

        if form.is_valid():
            review.text = request.POST.get('text')
            form.save() 
            return redirect('product_detail') 

    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'is_admin': request.user.is_staff,
        'product': product,
        'reviews': reviews,
        'form': form,  # Pass the form to the template
    }

    return render(request, 'product_detail.html', context)