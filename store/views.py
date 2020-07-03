from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse
import json
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    prdoucts = ProductDetail.objects.all()
    context = {
        'title': 'Home',
        'products': prdoucts,
        'cartItems': cartItems
    }
    return render(request, 'store/home.html', context)




class ProductDetailView(DetailView,SingleObjectMixin):
    model = ProductDetail

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        context = super().get_context_data(**kwargs)
        context['cartItems'] = cartItems
        return context

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print('Hedello')
    else:
        print('Hello')
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems,'title': 'Cart'}
    return render(request, 'store/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = ProductDetail.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item was added', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = data['form']['total']
        print(total, "   ", order.get_cart_total)
        order.transaction_id = transaction_id
        if float(total) == float(order.get_cart_total):
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            appt=data['shipping']['appt'],
            area=data['shipping']['area'],
            landmark=data['shipping']['landmark'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    else:
        print('User Not logged In')

    return JsonResponse('Payment Complete', safe=False)
