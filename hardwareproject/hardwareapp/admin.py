from django.contrib import admin
from . models import Stock, Sale,Register
# Register your models here.
admin.site.register(Stock)
admin.site.register(Sale)
admin.site.register(Register)