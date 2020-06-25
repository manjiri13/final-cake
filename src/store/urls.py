from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('details/',views.productDetailView, name='store-detail'),
]
