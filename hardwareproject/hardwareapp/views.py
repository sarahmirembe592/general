from django.shortcuts import render, redirect
from hardwareapp.models import Stock

# Create your views here.
def home(request):
    # we fetch all the data
    all_stock = Stock.objects.all()
    context ={
        'stock': all_stock, 
    }
    return render(request, 'home.html', context)


def add(request):
    if request.method == "POST":
        payload = request.POST
        item_name = payload.get('item_name')
        unit = payload.get('unit') 
        quantity = payload.get('quantity')
        unit_cost = payload.get('unit_cost')
        selling_price = payload.get('selling_price')
        stock_date = payload.get('stock_date') 
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
        NewStock.stock_date = stock_date
        NewStock.supplier = supplier
        NewStock.specification = specification
        NewStock.payment_mode = payment_mode
        NewStock.save()
        return redirect('home')
    return render(request,'add.html')