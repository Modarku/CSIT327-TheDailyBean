from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .forms import ReviewForm
from home.models import Product, ProductSubscription, Review
from payment.models import Order
from favorites.models import Favorite
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib import messages
import json

# Create your views here.

def view_products(request):
    user = request.user
    is_authenticated = user.is_authenticated
    page = request.GET.get('page', 'products')
    template = 'subscriptions.html' if page == 'subscriptions' else 'products.html'
    has_onebean = False
    has_weeklybean = False

    if is_authenticated:
        product_subscriptions = ProductSubscription.objects.filter(user=user)

        for product_subscription in product_subscriptions:
            if product_subscription.subscription_type == 'Onebean': has_onebean = True
            if product_subscription.subscription_type == 'Weeklybean': has_weeklybean = True

    context = {
        'is_authenticated': is_authenticated,
        'is_admin': request.user.is_staff,
        'products': Product.objects.all(),
        'has_onebean': has_onebean,
        'has_weeklybean': has_weeklybean,

    }
    return render(request, template, context)

def product_detail(request, id):
    user = request.user
    is_authenticated = user.is_authenticated
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=id).order_by('-id')
    favorites = Favorite.objects.filter(product=product)
    is_favorited = False
    orders = None
    is_break = False

    if is_authenticated: 
        orders = Order.objects.filter(user=user)
        is_favorited = favorites.filter(user=request.user).exists()
        is_break = any(order.product.id == product.id for order in orders)
    
    #Product average rating helper function
    product_rating_helper(product)

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
        'user': user,
        'is_authenticated': is_authenticated,
        'is_admin': request.user.is_staff,
        'product': get_object_or_404(Product, id=id),
        'orders' : orders,
        'reviews': reviews,
        'form' : form,
        'is_break' : is_break,
        'is_favorited' : is_favorited,
        'favorites_count' : favorites.count
    }
    return render(request, 'product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    quantity = int(request.POST.get('quantity', 1))
    
    # added this to stack existing products
    existing_order = Order.objects.filter(product=product, user=user, date_paid=None).first()
    if existing_order:
        existing_order.product_amount += quantity
        existing_order.total = existing_order.product_amount * product.price
        existing_order.save()
    else:
        total_price = product.price * quantity
        Order.objects.create(
            product=product,
            user=user,
            product_amount=quantity,
            total=total_price,
            date_paid=None
        )

    messages.success(request, f'Added {quantity} of {product.product_name} to your Cart.', extra_tags='carted')
    
    return redirect('product_detail', product_id)

def search_products(request):
    query = request.GET.get('q') 
    template = request.GET.get('page', 'products.html')

    products = Product.objects.filter(product_name__icontains=query) if query else Product.objects.all()

    return render(request, template, {'products': products, 'query': query})

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.all()
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products.html', context)

@login_required
def add_to_subscription(request):
    
    user = request.user
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id_list = [int(pid) for pid in data.get('product_ids', '').split(',')]
            
            if len(product_id_list) == 1:
                subscription_type = 'Onebean'
                price = 349.00
            elif len(product_id_list) == 5:
                subscription_type = 'Weeklybean'
                price = 999.00
            else:
                subscription_type = 'Choicebean'
                price = 1299.00

            for product_id in product_id_list:
                product = get_object_or_404(Product, id=product_id)
                
                ProductSubscription.objects.create(
                    user=user,
                    product=product,
                    subscription_type=subscription_type,
                    price=price,
                    next_monthly = timezone.now()
                )
                
            return JsonResponse({'message': 'Subscription added successfully.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

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
        'form': form,
    }

    return render(request, 'product_detail.html', context)

# Creates ratings for products
def product_rating_helper(product):
    avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    product.rating = avg_rating if avg_rating is not None else 0   
    product.save()
