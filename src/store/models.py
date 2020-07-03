from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    name = models.CharField(max_length = 50)
    egg = models.BooleanField(default = True)
    image = models.ImageField(default='default.jpg',
                              upload_to='product_images')

    def __str__(self):
        return self.name

    @property
    def get_price_1kg(self):
        products = self.product_set.all()
        price_list = [product.get_price for product in products if product.size == 0.5]
        price = price_list[0]
        return price

    def get_price_size_all(self):
        products = self.product_set.all()
        p_size_list = [product.get_price_size for product in products]
        return p_size_list
    
    
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk , 'slug': self.name})
    

class Product(models.Model):
    productdetails = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    size = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.productdetails.name + str(self.size))
    
    @property
    def get_price(self):
        price = int(self.price)
        return price
    
    @property
    def get_price_size(self):
        size = self.size
        price = int(self.price)
        return size,price



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False)

    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.customer.username + str(self.id))
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        totalquantity = sum([item.quantity for item in orderitems])
        return totalquantity

class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    appt = models.CharField(max_length=50, null=False)
    area = models.CharField(max_length=100, null=False)
    landmark = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zipcode = models.CharField(max_length=50, null=False)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.customer.name + self.appt)
