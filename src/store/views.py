from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
# Create your views here.


def home(request):
    prdoucts = ProductDetail.objects.all()
    context = {
        'title': 'Home',
        'products': prdoucts
    }
    return render(request, 'store/home.html', context)


def productDetailView(request, ):  #id = None
    # product = get_object_or_404(ProductDetail, id=id)
    context = {
        'title' : 'details',
        # 'product' : product, 
    }

    return render(request, 'store/details.html', context)
