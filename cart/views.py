import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_id=session_key, user=None)
    return cart

def cart_detail(request):
    cart = _get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, id=product_id)
            cart = _get_or_create_cart(request)
            
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            
            cart_count = sum(item.quantity for item in cart.items.all())
            return JsonResponse({'status': 'success', 'cart_count': cart_count, 'message': 'Added to cart'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def update_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            action = data.get('action')
            
            cart = _get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                
            cart_count = sum(item.quantity for item in cart_item.cart.items.all())
            subtotal = float(cart_item.total_price)
            cart_total = sum(float(item.total_price) for item in cart_item.cart.items.all())
                
            return JsonResponse({
                'status': 'success', 
                'quantity': cart_item.quantity,
                'subtotal': subtotal,
                'cart_total': cart_total,
                'cart_count': cart_count
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            cart = _get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.delete()
            
            cart_count = sum(item.quantity for item in cart.items.all())
            cart_total = sum(float(item.total_price) for item in cart.items.all())
            
            return JsonResponse({'status': 'success', 'cart_count': cart_count, 'cart_total': cart_total})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)
