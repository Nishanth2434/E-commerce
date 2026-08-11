import time
import random
import requests
from decouple import config
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Review
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Seeds the database with categories, specific products, and fetches images from Unsplash.'

    def get_unsplash_image(self, search_term, fallback_text):
        access_key = config('UNSPLASH_ACCESS_KEY', default='')
        if not access_key:
            return f"https://placehold.co/400x400?text={fallback_text}"
            
        url = f"https://api.unsplash.com/search/photos?query={search_term}&per_page=1&orientation=squarish"
        headers = {'Authorization': f'Client-ID {access_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    return data['results'][0]['urls']['regular']
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to fetch Unsplash image for '{search_term}': {e}"))
            
        return f"https://placehold.co/400x400?text={fallback_text}"

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        if not config('UNSPLASH_ACCESS_KEY', default=''):
            self.stdout.write(self.style.WARNING("UNSPLASH_ACCESS_KEY is not set. Falling back to placehold.co images."))

        # Create superuser
        user, created = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@example.com'
        })
        if created:
            user.set_password('admin123')
            user.save()
            Profile.objects.get_or_create(user=user, defaults={'phone':'1234567890', 'city':'Metropolis'})
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created.'))
        else:
            self.stdout.write('Superuser "admin" already exists.')

        # Delete existing data to ensure clean seed
        Product.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'keyword': 'electronics shopping category flat lay'},
            {'name': 'Fashion', 'slug': 'fashion', 'keyword': 'fashion shopping category flat lay'},
            {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'keyword': 'home and kitchen shopping category flat lay'},
            {'name': 'Books', 'slug': 'books', 'keyword': 'books shopping category flat lay'},
            {'name': 'Beauty', 'slug': 'beauty', 'keyword': 'beauty shopping category flat lay'},
            {'name': 'Sports', 'slug': 'sports', 'keyword': 'sports shopping category flat lay'},
        ]

        category_objs = {}
        for cat_data in categories_data:
            image_url = self.get_unsplash_image(cat_data['keyword'], cat_data['slug'])
            cat = Category.objects.create(
                name=cat_data['name'],
                slug=cat_data['slug'],
                image=image_url
            )
            category_objs[cat.name] = cat
            self.stdout.write(self.style.SUCCESS(f"Fetched image for Category: {cat.name} (OK)"))
            time.sleep(0.5)

        # Exact Products Data
        products_data = [
            ("Electronics", "Wireless Bluetooth Headphones", "wireless headphones product", 2999, 2199),
            ("Electronics", "Wireless Mouse", "computer wireless mouse", 799, 599),
            ("Electronics", "27-inch LED Monitor", "computer monitor desk", 15999, 13499),
            ("Electronics", "Smartphone 128GB", "smartphone front screen", 21999, 18999),
            ("Electronics", "Bluetooth Portable Speaker", "portable bluetooth speaker", 1999, 1499),
            ("Electronics", "Laptop Backpack", "laptop backpack bag", 1299, 999),
            ("Fashion", "Men's Cotton T-Shirt", "plain cotton tshirt folded", 499, 349),
            ("Fashion", "Women's Denim Jacket", "denim jacket flat lay", 2199, 1699),
            ("Fashion", "Running Shoes", "running shoes pair", 2499, 1899),
            ("Fashion", "Leather Wallet", "leather wallet product", 899, 649),
            ("Fashion", "Analog Wrist Watch", "analog wrist watch", 1599, 1199),
            ("Fashion", "Sunglasses", "sunglasses product photo", 999, 749),
            ("Home & Kitchen", "Non-stick Frying Pan", "non stick frying pan", 899, 649),
            ("Home & Kitchen", "Electric Kettle", "electric kettle appliance", 1299, 999),
            ("Home & Kitchen", "Ceramic Dinner Set", "ceramic plates dinner set", 1999, 1499),
            ("Home & Kitchen", "Bedsheet with Pillow Covers", "bedsheet folded pillow", 1099, 799),
            ("Home & Kitchen", "Table Lamp", "table lamp desk", 799, 599),
            ("Home & Kitchen", "Vacuum Cleaner", "vacuum cleaner appliance", 5999, 4499),
            ("Books", "The Alchemist (Paperback)", "paperback novel book cover", 299, 199),
            ("Books", "Atomic Habits", "book stack self help", 499, 349),
            ("Books", "Rich Dad Poor Dad", "finance book cover", 349, 249),
            ("Books", "Python Programming Guide", "programming book laptop", 799, 599),
            ("Beauty", "Face Moisturizer Cream", "face cream jar cosmetic", 399, 299),
            ("Beauty", "Herbal Shampoo", "shampoo bottle product", 349, 249),
            ("Beauty", "Lipstick Set", "lipstick makeup product", 599, 449),
            ("Beauty", "Perfume 100ml", "perfume bottle product", 1499, 1099),
            ("Sports", "Yoga Mat", "rolled yoga mat", 799, 599),
            ("Sports", "Cricket Bat", "cricket bat equipment", 1999, 1499),
            ("Sports", "Football", "soccer football ball", 899, 649),
            ("Sports", "Adjustable Dumbbells", "dumbbell weights pair", 2999, 2299),
        ]

        # Review Templates
        positive_reviews = [
            "Absolutely love this product! Highly recommended.",
            "Great quality for the price. I've been using it every day.",
            "Exceeded my expectations. Will definitely buy again.",
            "Works perfectly as described. Very satisfied with my purchase."
        ]
        mixed_reviews = [
            "It's decent, but I wish the build quality was a bit better.",
            "Good product overall, but delivery was a bit slow.",
            "Meets expectations. Nothing too special, but gets the job done."
        ]

        for item in products_data:
            category_name, product_name, keyword, price, discount_price = item
            
            slug = product_name.lower().replace(" ", "-").replace("'", "").replace("(", "").replace(")", "").replace("&", "and")
            
            # Fetch image from Unsplash
            image_url = self.get_unsplash_image(keyword, slug)
            
            product = Product.objects.create(
                category=category_objs[category_name],
                name=product_name,
                slug=slug,
                description=f"This high-quality {product_name} is perfect for your needs. Explore more from our {category_name} collection.",
                price=price,
                discount_price=discount_price,
                stock_quantity=random.randint(10, 100),
                image=image_url
            )
            
            self.stdout.write(self.style.SUCCESS(f"Fetched image for: {product_name} (OK)"))
            time.sleep(0.5)

            # Generate 2-3 reviews
            num_reviews_to_add = random.randint(2, 3)
            total_rating = 0
            
            for _ in range(num_reviews_to_add):
                rating = random.choice([4, 5]) if random.random() > 0.3 else 3
                comment = random.choice(positive_reviews if rating >= 4 else mixed_reviews)
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    comment=f"{comment} Really fits well for a {product_name}."
                )
                total_rating += rating
                
            product.num_reviews = num_reviews_to_add
            product.rating = round(total_rating / num_reviews_to_add, 1)
            product.save()

        self.stdout.write(self.style.SUCCESS('Database seeding complete with Unsplash images!'))
