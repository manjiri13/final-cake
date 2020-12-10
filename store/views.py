from .models import *
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserForm,CustomerForm
from django.contrib import messages
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
    messages.warning(request,'Zero Contact Delivery Due to Covid-19 Pandemic')
    context = {
        'title': 'Home',
        'products': prdoucts,
        'cartItems': cartItems,
    }
    return render(request, 'store/home.html', context)





def menu(request):
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
        'title': 'Menu',
        'products': prdoucts,
        'cartItems': cartItems,
    }
    return render(request, 'store/menu.html', context)

def OnOrder(request):
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
    context = {
        'title': 'On Order',
        'cartItems': cartItems
    }
    return render(request, 'store/on_order.html', context)



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

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request, f'Sucessfully LoggedIn !!')
                return redirect('store-home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'store/login.html', {})

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('store-home'))

def Register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        customer_form = CustomerForm(data=request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.name = user.username
            customer.save()
            registered = True
        else:
            print(user_form.errors,customer_form.errors)
        if registered:
            messages.success(request, f'Account created Now you can Log In !!')
            return redirect('login')
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    return render(request,'store/register.html',
                          {'user_form':user_form,
                          'customer_form':customer_form,
                           'registered':registered})