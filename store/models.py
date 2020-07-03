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
    price = models.DecimalField(max_digits=6, decimal_places=2,default = 199)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk , 'slug': self.name})
    


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False)

    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.customer.name + str(self.id))
    
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
        ProductDetail, on_delete=models.SET_NULL, null=True, blank=True)
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
