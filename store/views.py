from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .models import Product, CartItem, Order, OrderItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > product.stock:
            messages.error(request, 'Not enough stock available.')
            return redirect('product_detail', pk=pk)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product,
            defaults={'quantity': 0}
        )
        new_qty = cart_item.quantity + quantity
        if new_qty > product.stock:
            messages.error(request, 'Not enough stock available.')
            return redirect('product_detail', pk=pk)
        cart_item.quantity = new_qty
        cart_item.save()
        messages.success(request, f'{product.name} added to cart.')
    return redirect('product_list')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def update_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > cart_item.product.stock:
            messages.error(request, 'Not enough stock available.')
        elif quantity < 1:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    return redirect('view_cart')


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


@login_required
@transaction.atomic
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('view_cart')

    if request.method == 'POST':
        address = request.POST.get('address', '')
        if not address:
            messages.error(request, 'Please provide a shipping address.')
            return redirect('checkout')

        total = Decimal('0.00')
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f'Not enough stock for {item.product.name}.')
                return redirect('view_cart')
            total += item.total_price()

        order = Order.objects.create(
            user=request.user,
            total=total,
            address=address
        )

        for item in cart_items:
            product = item.product
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity
            )
            product.stock -= item.quantity
            product.save()

        cart_items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', pk=order.pk)

    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        try:
            validate_password(password)
        except ValidationError as e:
            for err in e:
                messages.error(request, err)
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('product_list')
    return render(request, 'store/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('product_list')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def user_logout(request):
    logout(request)
    return redirect('product_list')
