from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

from .models import SupportTicket, Registry, RegistryItem, SellerApplication

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)

@admin.register(Registry)
class RegistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'event_type', 'created_at')
    list_filter = ('event_type', 'created_at')

@admin.register(RegistryItem)
class RegistryItemAdmin(admin.ModelAdmin):
    list_display = ('registry', 'product', 'added_at')

@admin.register(SellerApplication)
class SellerApplicationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'email', 'category', 'created_at')
    list_filter = ('category', 'created_at')
