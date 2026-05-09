# Accessing forms in django so that we can use it in our own forms/edit forms, etc
from django import forms
# Accessing the models that we are going to use with the forms
from . models import *
# Modeling a form which is supposed to be based on the model
# The form name should end with the (Form)
class StockeditForm(forms.ModelForm):
    # Creating meta class () 
    class Meta():
        model = Stock
        fields = ["quantity","date","supplier","specification","payment_mode"]

class DepositeditForm(forms.ModelForm):
    # Creating meta class () 
    class Meta():
        model = Register
        fields = ["amount","date","payment_method"]

