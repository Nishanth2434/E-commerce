from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review, SupportTicket, Registry, RegistryItem, SellerApplication

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

def deals(request):
    products = Product.objects.filter(discount_price__isnull=False)
    products = products.annotate(
        discount_percent=ExpressionWrapper(
            ((F('price') - F('discount_price')) / F('price')) * 100,
            output_field=FloatField()
        )
    ).order_by('-discount_percent')
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/deals.html', {'page_obj': page_obj})

def customer_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            SupportTicket.objects.create(name=name, email=email, message=message)
            return render(request, 'products/customer_service.html', {'success': True})
    return render(request, 'products/customer_service.html')

@login_required
def registry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        event_type = request.POST.get('event_type')
        if name and event_type:
            reg = Registry.objects.create(user=request.user, name=name, event_type=event_type)
            return redirect('products:registry_detail', id=reg.id)
    registries = Registry.objects.filter(user=request.user)
    return render(request, 'products/registry.html', {'registries': registries})

def registry_detail(request, id):
    registry = get_object_or_404(Registry, id=id)
    return render(request, 'products/registry_detail.html', {'registry': registry})

@login_required
def add_to_registry(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        registry_id = request.POST.get('registry_id')
        if registry_id:
            registry = get_object_or_404(Registry, id=registry_id, user=request.user)
            RegistryItem.objects.get_or_create(registry=registry, product=product)
            return redirect('products:registry_detail', id=registry.id)
    return redirect('products:product_detail', slug=product.slug)

def gift_cards(request):
    gift_cards = Product.objects.filter(category__name='Gift Cards')
    return render(request, 'products/gift_cards.html', {'gift_cards': gift_cards})

def sell(request):
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        category = request.POST.get('category')
        if business_name and email:
            SellerApplication.objects.create(
                business_name=business_name, email=email, phone=phone, category=category
            )
            return render(request, 'products/sell.html', {'success': True})
    return render(request, 'products/sell.html')
