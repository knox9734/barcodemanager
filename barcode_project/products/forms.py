# forms.py
from django import forms
from .models import Product,Inventory

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

class StockUpdateForm(forms.ModelForm):
    change = forms.IntegerField(label="Change in stock (use negative to reduce)", required=True)

    class Meta:
        model = Inventory
        fields = ['change']

    def save(self, commit=True):
        inventory = super().save(commit=False)
        inventory.stock_quantity += self.cleaned_data['change']
        if inventory.stock_quantity < 0:
            inventory.stock_quantity = 0  # Avoid negative stock
        if commit:
            inventory.save()
        return inventory