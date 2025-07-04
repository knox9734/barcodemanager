# admin.py
from django.contrib import admin
from .models import Product,Inventory

admin.site.register(Product)
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'stock_quantity', 'last_updated']
    search_fields = ['product__name']
