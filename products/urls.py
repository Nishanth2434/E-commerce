from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('deals/', views.deals, name='deals'),
    path('customer-service/', views.customer_service, name='customer_service'),
    path('registry/', views.registry, name='registry'),
    path('registry/<int:id>/', views.registry_detail, name='registry_detail'),
    path('registry/add/<int:product_id>/', views.add_to_registry, name='add_to_registry'),
    path('gift-cards/', views.gift_cards, name='gift_cards'),
    path('sell/', views.sell, name='sell'),
]
