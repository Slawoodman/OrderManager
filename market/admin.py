from django.contrib import admin
from .models import Product, OrderItem

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'discounted_price', 'created_date']
#     list_filter = ['price', 'created_date']
#     readonly_fields = ('created_date',)

admin.site.register(Product)
admin.site.register(OrderItem)
