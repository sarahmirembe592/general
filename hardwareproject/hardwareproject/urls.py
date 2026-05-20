"""
URL configuration for hardwareproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from hardwareapp import views

urlpatterns = [
    # Root URL - redirect to dashboard
    path('', RedirectView.as_view(url='dashboard/', permanent=False), name='home'),
    
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Stock URLs
    path('stock_list/', views.stock_list, name='stock_list'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('add_stock/<int:pk>/', views.stock_review, name='stock_review'),
    
    # Sales URLs
    path('sales_list/', views.sales_list, name='sales_list'),
    path('add_sale/', views.add_sale, name='add_sale'),
    path('sales_list/<int:pk>/', views.sale_detail, name='sale_detail'),
    
    # Customer URLs
    path('customer_list/', views.customer_list, name='customer_list'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('customer_list/<int:pk>/', views.deposit_review, name='deposit_review'),
    path('customer_list/<int:pk>/edit/', views.customer_detail, name='customer_detail'),
    
    # Authentication & Other
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout_view'),
]