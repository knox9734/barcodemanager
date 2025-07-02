# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, BulkProductForm,BarcodeGenerateForm
from django.forms import formset_factory
from django.contrib import messages
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import random
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (400, 200), color='white')
draw = ImageDraw.Draw(img)

font_folder = os.path.join(settings.MEDIA_ROOT, 'fonts')
fontname = f'FMAbhaya.ttf'
fontpath = os.path.join(font_folder, fontname)
# font = ImageFont.truetype(fontpath, 20)
font = ImageFont.truetype(fontpath, 24)
font_bold = ImageFont.truetype(fontpath, 26)
font_english = ImageFont.truetype("arial.ttf", 24)



def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def bulk_add_products(request):
    ProductFormSet = formset_factory(BulkProductForm, extra=5)
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    product = Product(**form.cleaned_data)
                    product.save()
            return redirect('product_list')
    else:
        formset = ProductFormSet()
    return render(request, 'products/bulk_add_products.html', {'formset': formset})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


def generate_barcodes(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = BarcodeGenerateForm(request.POST)

        if form.is_valid():
            product.price = form.cleaned_data['price']
            product.manufacture_date = form.cleaned_data['manufacture_date']
            product.expiry_date = form.cleaned_data['expiry_date']
            product.save()

            quantity = form.cleaned_data['quantity']

            product_folder = os.path.join(settings.MEDIA_ROOT, 'barcodes', f'{product.name}')
            os.makedirs(product_folder, exist_ok=True)

            for i in range(quantity):
                barcode_number = product.generate_unique_ean13()
                ean = barcode.get('ean13', barcode_number, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                barcode_image = Image.open(buffer)

                # Create a label (400x300) white background
                label = Image.new('RGB', (400, 300), 'white')
                draw = ImageDraw.Draw(label)


                # draw.text((10, 10), "කපුකොටුව සහල්", font=font_bold, fill="black")
                # draw.text((10, 40), product.name, font=font_bold, fill="black")
                # draw.text((10, 80), f"Price: {product.price}", font=font, fill="black")
                # draw.text((10, 110), f"MFD: {product.manufacture_date}", font=font, fill="black")
                # draw.text((10, 140), f"EXP: {product.expiry_date}", font=font, fill="black")
                draw.text((10, 10), "lmqfldgqj iy,a", font=font_bold, fill="black")
                draw.text((10, 40), f" {product.name}", font=font_english, fill="black")
                draw.text((10, 80), f"ñ, • re ¡ {product.price}", font=font, fill="black")
                draw.text((10, 110), f"ksIamdÈ; Èkh {product.manufacture_date.strftime('%Y-%m-%d')}", font=font, fill="black")
                draw.text((10, 140), f"l,a bl=;ajk Èkh  {product.expiry_date.strftime('%Y-%m-%d')}", font=font, fill="black")


                # Paste the barcode image
                label.paste(barcode_image.resize((360, 96)), (50, 180))


                filename = f'{barcode_number}_{i+1}.png'
                filepath = os.path.join(product_folder, filename)
                label.save(filepath)

            messages.success(request, f'{quantity} barcode label(s) generated.')
            return redirect('product_detail', pk=product.pk)

    else:
        form = BarcodeGenerateForm()

    return render(request, 'products/generate_barcodes.html', {'form': form, 'product': product})