from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'user__username', 'phone')
    inlines = [OrderItemInline]
