from django.db import models
from django.urls import reverse
from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)
    
    def get_absolute_url(self):
        return reverse('product_type', args=[str(self.id)])


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, related_name="products", null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=100)
    stock = models.IntegerField(default=0)

    STATUS_CHOICES = [
        ("AVA", "Available"),
        ("SAL", "On Sale"),
        ("OUT", "Out of Stock"),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default="AVA", max_length=3)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])
    

class Transaction(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)

    STATUS_CHOICES = [
        ("On Cart", "On Cart"),
        ("To Pay", "To Pay"),
        ("To Ship", "To Ship"),
        ("To Receive", "To Receive"),
        ("Delivered", "Delivered"),
    ]
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="On Cart")

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        buyer_name = self.buyer.name if self.buyer else "Unknown Buyer"
        return f'{self.amount} x {product_name} - {buyer_name}'
