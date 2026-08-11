from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category, Review

def home(request):
    deals = Product.objects.filter(discount_price__isnull=False).order_by('?')[:4]
    products = Product.objects.all().order_by('-created_at')[:12]
    categories = Category.objects.all()
    return render(request, 'products/home.html', {
        'deals': deals,
        'products': products,
        'categories': categories,
    })

def product_list(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    sort = request.GET.get('sort', '-created_at')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if sort in ['price', '-price', '-rating', '-created_at']:
        products = products.order_by(sort)

    categories = Category.objects.all()
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
        'sort': sort,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating:
            Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
            return redirect('products:product_detail', slug=product.slug)
            
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })
