import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shophub.settings')
django.setup()

from products.models import Category, Product

# Create Gift Cards category
gc_cat, created = Category.objects.get_or_create(
    name='Gift Cards',
    slug='gift-cards',
    defaults={'image': 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=800&q=80'}
)

if created:
    print("Created Gift Cards category")

prices = [500, 1000, 2500, 5000]
for p in prices:
    Product.objects.get_or_create(
        category=gc_cat,
        name=f"ShopHub Gift Card - ₹{p}",
        slug=f"gift-card-{p}",
        defaults={
            'price': p,
            'stock_quantity': 9999,
            'description': f"A ₹{p} Gift Card for ShopHub. The perfect gift for anyone.",
        }
    )

print("Gift cards seeded.")
