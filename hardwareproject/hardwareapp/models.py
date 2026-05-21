from django.db import models

class Stock(models.Model):
    item_name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_cost = models.IntegerField()
    selling_price = models.IntegerField()
    date = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    specification = models.CharField(max_length=255)
    payment_mode = models.CharField(max_length=255)

    def __str__(self):
        return self.item_name


class Sale(models.Model):
    customer_name = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    # Transport fields
    wants_delivery = models.BooleanField(default=False)
    within_10km = models.BooleanField(default=False)
    transport_charge = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)

    def __str__(self):
        return self.customer_name


class Register(models.Model):
    name = models.CharField(max_length=255)
    nin = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)
    date = models.CharField(max_length=255, null=True)
    select_product = models.CharField(max_length=255)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=255)