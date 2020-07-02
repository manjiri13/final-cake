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
