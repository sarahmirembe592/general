from django.db import models

# Create your models here.
class Stock(models.Model):
    item_name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_cost = models.IntegerField()
    selling_price = models.IntegerField()
    stock_date = models.DateTimeField(auto_now_add=True)
    supplier = models.TextField()
    specification = models.CharField(max_length=255)
    payment_mode = models.CharField(max_length=255)