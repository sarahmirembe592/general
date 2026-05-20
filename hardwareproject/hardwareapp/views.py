from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from hardwareapp.models import Stock, Sale,Register
from . forms import *
# importing a decorator(it's a function that must be run before running another function)
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,logout
from django.db.models import Sum, Q

# Create your views here.
@login_required
def stock_list(request):
    # we fetch all the data
    all_stock = Stock.objects.all()

    search_query = request.GET.get('search', '')

    if search_query:
        all_stock = all_stock.filter(
            Q(item_name__icontains=search_query) |
            Q(supplier__icontains=search_query)
        )

    total_unit_cost = all_stock.aggregate(Sum('unit_cost'))['unit_cost__sum'] or 0
    total_selling_price = all_stock.aggregate(Sum('selling_price'))['selling_price__sum'] or 0

  


    context = {
        'stock': all_stock, 
        'search_query': search_query, 
        'total_unit_cost': total_unit_cost,
        'total_selling_price': total_selling_price,  
    }
    return render(request, 'stock_list.html', context)

@login_required
def add_stock(request):
    if request.method == "POST":
        payload = request.POST
        item_name = payload.get('item_name')
        unit = payload.get('unit') 
        quantity = payload.get('quantity')
        unit_cost = payload.get('unit_cost')
        selling_price = payload.get('selling_price')
        date = payload.get('date')
        supplier = payload.get('supplier')
        specification = payload.get('specification')
        payment_mode = payload.get('payment_mode')

        # New stock
        NewStock = Stock()
        NewStock.item_name = item_name
        NewStock.unit = unit
        NewStock.quantity = quantity
        NewStock.unit_cost = unit_cost
        NewStock.selling_price = selling_price
        NewStock.date = date
        NewStock.supplier = supplier
        NewStock.specification = specification
        NewStock.payment_mode = payment_mode
        NewStock.save()
        return redirect('stock_list')
    return render(request,'add_stock.html')

@login_required
def sales_list(request):
    # we fetch all the data
    sales = Sale.objects.all()

    search_query = request.GET.get('search', '')
    
    if search_query:
          sales = sales.filter(
            Q(product_name__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(category__icontains=search_query)
        )

# aggregate() is used to calculate something from many rows.
# The result is a dictionary where the key is 'total_price__sum' and the value is the calculated sum. 
    total_sales = sales.aggregate(
        Sum('total_price'))
    
    ['total_price__sum']
    total_prices = [total_price for total_price in sales.values_list('total_price', flat=True)]
    grand_total = sum(total_prices)

    context = {
        'sale': sales,
        'total_sales': total_sales,
        'search_query': search_query,
        'total_prices': total_prices,
        'grand_total': grand_total,
    }

    return render(request, 'sales_list.html', context)
  


@login_required
def add_sale(request):
    if request.method == 'POST':
        payload = request.POST
        customer_name = payload.get('customer_name')
        phone_number = payload.get('phone_number')
        address = payload.get('address')
        category = payload.get('category')
        product_name = payload.get('product_name')
        # product_name2 = payload.get('product_name2')
        quantity = int(payload.get('quantity'))
        unit_price = int(payload.get('unit_price'))
        total_price = payload.get('total_price')
        payment_method = payload.get('payment_method')
        total_price = quantity * unit_price

        # New sale made
        NewSale = Sale()
        NewSale.customer_name = customer_name
        NewSale.phone_number = phone_number
        NewSale.address = address
        NewSale.category = category
        NewSale.product_name = product_name
        NewSale.quantity = quantity
        NewSale.unit_price = unit_price
        NewSale.total_price = total_price
        NewSale.payment_method = payment_method
        NewSale.save()
        return redirect('sales_list')
    return render(request,'add_sale.html')


@login_required
def customer_list(request):
    all_register = Register.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        all_register = all_register.filter(
            Q(name__icontains=search_query) |
            Q(select_product__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    grand_total = all_register.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'register': all_register,
        'search_query': search_query,
        'grand_total': grand_total,
    }
    return render(request, 'customer_list.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        payload = request.POST
        name = payload.get('name')
        nin = payload.get('nin')
        phone = payload.get('phone')
        address = payload.get('address')
        date = payload.get('date')
        select_product = payload.get('select_product')
        amount = payload.get('amount')
        payment_method = payload.get('payment_method')


        # NewRegister made
        NewRegister = Register()
        NewRegister.name = name
        NewRegister.nin = nin
        NewRegister.phone = phone
        NewRegister.address = address
        NewRegister.date = date
        NewRegister.select_product = select_product
        NewRegister.amount = amount
        NewRegister.payment_method = payment_method

        NewRegister.save()
        return redirect('customer_list')
    return render(request,'add_customer.html')


# Receipt for sales
@login_required
def sale_detail(request,pk):
    # Fetching all specific entry using primary key(pk)
    entry = get_object_or_404(Sale,pk=pk)
    return render(request,'receipt.html',{'entry': entry})
# Receipt for credit scheme

@login_required
def customer_detail(request,pk):
    # Fetching all specific entry using primary key(pk)
    entry = get_object_or_404(Register,pk=pk)
    return render(request,'customer_edit.html',{'entry': entry})


# Editing Stock
@login_required
def stock_review(request,pk):
    # Handling the data from the edit form
    # Fetch stock item or return 404 if not found
    entry = get_object_or_404(Stock,pk=pk)
    form = StockeditForm(request.POST, instance = entry)

    if request.method == 'POST':
        # Save changes if form data is valid
        if form.is_valid():
            form.save()
            return redirect('add_stock')
    else:
        form = StockeditForm(instance = entry)
    
    return render(request,'stock_edit.html',{'form': form})


# edit receipt for customer deposit
@login_required
def deposit_review(request,pk):
    # Handling the data from the edit form
    entry = get_object_or_404(Register,pk=pk)
    form = DepositeditForm(request.POST, instance = entry)

    if request.method == 'POST':
       
        if form.is_valid():
            form.save()
            return redirect('add_customer')
    else:
        form = DepositeditForm(instance = entry)

        print("something went wrong")
    
    return render(request,'deposit_edit.html',{'form': form})



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
    


    



