from django.contrib import admin
from .models import ProductType, Product, Transaction

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'product_type', 'price']

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)