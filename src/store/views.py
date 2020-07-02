from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
# Create your views here.


def home(request):
    prdoucts = ProductDetail.objects.all()
    context = {
        'title': 'Home',
        'products': prdoucts
    }
    return render(request, 'store/home.html', context)




class ProductDetailView(DetailView):
    model = ProductDetail

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)
