from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('menu/', views.menu, name='store-menu'),
    path('order/', views.OnOrder, name='store-order'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='store-detail'),
    path('cart/',views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('register/',views.Register,name='register'),
]
