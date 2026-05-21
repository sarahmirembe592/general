from django.shortcuts import render, redirect, get_object_or_404
from hardwareapp.models import Stock, Sale, Register
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.db.models import Sum, Q


# Transport calculation
def calculate_transport(within_10km, order_total):
    if within_10km and order_total >= 500000:
        return 0       # Free delivery
    return 30000       # Flat charge


@login_required
def stock_list(request):
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
        NewStock = Stock()
        NewStock.item_name = payload.get('item_name')
        NewStock.unit = payload.get('unit')
        NewStock.quantity = payload.get('quantity')
        NewStock.unit_cost = payload.get('unit_cost')
        NewStock.selling_price = payload.get('selling_price')
        NewStock.date = payload.get('date')
        NewStock.supplier = payload.get('supplier')
        NewStock.specification = payload.get('specification')
        NewStock.payment_mode = payload.get('payment_mode')
        NewStock.save()
        return redirect('stock_list')
    return render(request, 'add_stock.html')


@login_required
def sales_list(request):
    sales = Sale.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        sales = sales.filter(
            Q(product_name__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    grand_total = sales.aggregate(Sum('grand_total'))['grand_total__sum'] or 0

    context = {
        'sale': sales,
        'search_query': search_query,
        'grand_total': grand_total,
    }
    return render(request, 'sales_list.html', context)


@login_required
def add_sale(request):
    if request.method == 'POST':
        payload = request.POST
        quantity = round(float(payload.get('quantity')))
        unit_price = round(float(payload.get('unit_price')))
        total_price = quantity * unit_price

        # Transport logic
        wants_delivery = payload.get('wants_delivery') == 'on'
        within_10km = payload.get('within_10km') == 'on'
        transport_charge = 0

        if wants_delivery:
            transport_charge = calculate_transport(within_10km, total_price)

        grand_total = total_price + transport_charge

        NewSale = Sale()
        NewSale.customer_name = payload.get('customer_name')
        NewSale.phone_number = payload.get('phone_number')
        NewSale.address = payload.get('address')
        NewSale.category = payload.get('category')
        NewSale.product_name = payload.get('product_name')
        NewSale.quantity = quantity
        NewSale.unit_price = unit_price
        NewSale.total_price = total_price
        NewSale.payment_method = payload.get('payment_method')
        NewSale.wants_delivery = wants_delivery
        NewSale.within_10km = within_10km
        NewSale.transport_charge = transport_charge
        NewSale.grand_total = grand_total
        NewSale.save()
        return redirect('sales_list')
    return render(request, 'add_sale.html')


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
        NewRegister = Register()
        NewRegister.name = payload.get('name')
        NewRegister.nin = payload.get('nin')
        NewRegister.phone = payload.get('phone')
        NewRegister.address = payload.get('address')
        NewRegister.date = payload.get('date')
        NewRegister.select_product = payload.get('select_product')
        NewRegister.amount = payload.get('amount')
        NewRegister.payment_method = payload.get('payment_method')
        NewRegister.save()
        return redirect('customer_list')
    return render(request, 'add_customer.html')


@login_required
def sale_detail(request, pk):
    entry = get_object_or_404(Sale, pk=pk)
    return render(request, 'receipt.html', {'entry': entry})


@login_required
def customer_detail(request, pk):
    entry = get_object_or_404(Register, pk=pk)
    return render(request, 'customer_edit.html', {'entry': entry})


@login_required
def stock_review(request, pk):
    entry = get_object_or_404(Stock, pk=pk)
    form = StockeditForm(request.POST, instance=entry)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('add_stock')
    else:
        form = StockeditForm(instance=entry)

    return render(request, 'stock_edit.html', {'form': form})


@login_required
def deposit_review(request, pk):
    entry = get_object_or_404(Register, pk=pk)
    form = DepositeditForm(request.POST, instance=entry)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('add_customer')
    else:
        form = DepositeditForm(instance=entry)

    return render(request, 'deposit_edit.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')