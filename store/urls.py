from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='store-detail'),
    path('cart/',views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
]
