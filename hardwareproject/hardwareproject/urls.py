"""
URL configuration for hardwareproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hardwareapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # This url takes you to the list of all items in the Stock
    path('',views.home, name='home'),
    # This url leads you to the page that let's you add items in the Stock
    path('add/',views.add, name='add'),
    # This url takes you to the list of all items in the Sales
    path('home1/',views.home1, name='home1'),
    # This url leads you to the page that let's you add items in the Sale
    path('add1/',views.add1, name='add1'),
    # This url takes you to the list of all registered salary earners & their deposit
    path('home3/',views.home3, name='home3'),
    # his url leads you to the page that let's you add salary earners with their current deposits
    path('add3/',views.add3, name='add3'),
    # a view that will capture an id for a particular sale 
    path('home1/<int:pk>/',views.sale_detail, name='sale_detail'),
    path('<int:pk>/',views.stock_review, name='stock_review'),
    # T his url leads you editing deposit
    path('home3/<int:pk>/',views.deposit_review, name='deposit_review'),
    # This url leads you to the customer temp receipt
    path('home3/<int:pk>/edit/',views.customer_detail, name='customer_detail'),

]
