from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def merge_cart(sender, user, request, **kwargs):
    if request.session.session_key:
        try:
            session_cart = Cart.objects.get(session_id=request.session.session_key, user=None)
            user_cart, _ = Cart.objects.get_or_create(user=user)
            
            for item in session_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                if not created:
                    user_item.quantity += item.quantity
                else:
                    user_item.quantity = item.quantity
                user_item.save()
                
            session_cart.delete()
        except Cart.DoesNotExist:
            pass
