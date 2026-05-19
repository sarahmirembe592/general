from django.shortcuts import render, redirect, get_object_or_404
from hardwareapp.models import Stock, Sale,Register
from . forms import *
# importing a decorator(it's a function that must be run before running another function)
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,logout
from django.db.models import Sum

# Create your views here.
@login_required
def stock_list(request):
    # we fetch all the data
    all_stock = Stock.objects.all()
    context ={
        'stock': all_stock, 
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
# aggregate() is used to calculate something from many rows.
# The result is a dictionary where the key is 'total_price__sum' and the value is the calculated sum. 
    total_sales = sales.aggregate(
        Sum('total_price'))
    
    ['total_price__sum']

    context = {
        'sale': sales,
        'total_sales': total_sales
    }

    return render(request, 'sales_list.html', context)
  


@login_required
def add_sale(request):
    if request.method == 'POST':
        payload = request.POST
        customer_name = payload.get('customer_name')
        # phone_number = payload.get('phone_number')
        # address = payload.get('address')
        category = payload.get('category')
        product_name = payload.get('product_name')
        quantity = int(payload.get('quantity'))
        unit_price = int(payload.get('unit_price'))
        total_price = payload.get('total_price')
        payment_method = payload.get('payment_method')
        total_price = quantity * unit_price

        # New sale made
        NewSale = Sale()
        NewSale.customer_name = customer_name
        NewSale.category = category
        NewSale.product_name = product_name
        NewSale.quantity = quantity
        NewSale.unit_price = unit_price
        NewSale.total_price = total_price
        NewSale.payment_method = payment_method
        NewSale.save()
        return redirect('sale_list')
    return render(request,'add_sale.html')


@login_required
def customer_list(request):
    all_register = Register.objects.all()
    context = {
        'register': all_register,
    }
    return render(request, 'customer_list.html',context)


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
    return redirect('dashboard')
@login_required
def contact(request):
    return render(request, 'contact.html')
    


    



