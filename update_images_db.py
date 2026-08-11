import os
import shutil
import glob
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shophub.settings')
django.setup()

from products.models import Category, Product

artifact_dir = r"C:\Users\nisha\.gemini\antigravity\brain\1127449f-ede0-4717-a499-e8a25e1e953f"
media_dir = r"c:\Users\nisha\OneDrive\Desktop\projects\E-commerce\media"

if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Copy all jpg files from artifact dir to media dir
for img_path in glob.glob(os.path.join(artifact_dir, "*.jpg")):
    shutil.copy(img_path, media_dir)

# Update Categories
cat_mapping = {
    'Electronics': 'category_electronics',
    'Fashion': 'category_fashion',
    'Home & Kitchen': 'category_home_kitchen',
    'Books': 'category_books',
    'Beauty': 'category_beauty',
    'Sports': 'category_sports',
}

for cat_name, prefix in cat_mapping.items():
    # Find the copied file in media_dir
    files = [f for f in os.listdir(media_dir) if f.startswith(prefix) and f.endswith('.jpg')]
    if files:
        file_url = f"/media/{files[0]}"
        Category.objects.filter(name=cat_name).update(image=file_url)
        print(f"Updated category {cat_name} to {file_url}")

# Update specific products
prod_mapping = {
    'Herbal Shampoo': 'product_herbal_shampoo',
    'Sunglasses': 'product_sunglasses',
    'Non-stick Frying Pan': 'product_frying_pan',
    'Ceramic Dinner Set': 'product_dinner_set',
}

for prod_name, prefix in prod_mapping.items():
    files = [f for f in os.listdir(media_dir) if f.startswith(prefix) and f.endswith('.jpg')]
    if files:
        file_url = f"/media/{files[0]}"
        Product.objects.filter(name=prod_name).update(image=file_url)
        print(f"Updated product {prod_name} to {file_url}")

print("Images updated successfully!")
