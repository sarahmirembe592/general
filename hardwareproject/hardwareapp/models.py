from django.db import models


# Create your models here.
class Stock(models.Model):
    item_name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_cost = models.IntegerField()
    selling_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    supplier = models.TextField()
    specification = models.CharField(max_length=255)
    payment_mode = models.CharField(max_length=255)

    # Defining a method to describe how it should be seen by others
    def __str__(self):
        return self.item_name




class Sale(models.Model):
    customer_name = models.TextField()
    # phone_number = models.IntegerField(null=True,blank=True)
    # address = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255)
    product_name = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    # receipt_number = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    # name_of_sales_person = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.item_name  

# class Deposit(models.Model):
#     customer_nin = models.CharField(max_length=255)
#     select_product = models.CharField(max_length=255)
#     amount = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

class Register(models.Model):
    name = models.CharField(max_length=255)
    nin = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)
    select_product = models.CharField(max_length=255)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=255)

   


