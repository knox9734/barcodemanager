# forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category','product_code']

class BulkProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    category = forms.CharField(max_length=100, required=False)

class BarcodeGenerateForm(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    manufacture_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    quantity = forms.IntegerField(min_value=1, initial=1)
