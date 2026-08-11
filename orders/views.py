from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart
from accounts.models import Profile

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('products:home')
        
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('products:home')

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        
        cart_total = sum(float(item.total_price) for item in cart.items.all())
        shipping = 40.0 if cart_total < 499 else 0.0
        total_amount = cart_total + shipping
        
        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            phone=phone,
            total_amount=total_amount,
            payment_method=payment_method
        )
        
        # Create Order Items and decrease stock
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.discount_price if item.product.discount_price else item.product.price
            )
            # Decrease stock
            item.product.stock_quantity -= item.quantity
            item.product.save()
            
        # Clear Cart
        cart.items.all().delete()
        
        return redirect('orders:order_confirmation', order_id=order.id)
        
    cart_total = sum(float(item.total_price) for item in cart.items.all())
    shipping = 40.0 if cart_total < 499 else 0.0
    total = cart_total + shipping
    
    return render(request, 'orders/checkout.html', {
        'cart': cart, 
        'profile': profile,
        'cart_total': cart_total,
        'shipping': shipping,
        'total': total
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})
