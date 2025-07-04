# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Inventory
from .forms import ProductForm, BulkProductForm,BarcodeGenerateForm,StockUpdateForm
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
from django.db.models import Sum

#pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader
import io


img = Image.new('RGB', (400, 200), color='white')
draw = ImageDraw.Draw(img)

font_folder = os.path.join(settings.MEDIA_ROOT, 'fonts')
fontname = f'FMAbhaya.ttf'
fontpath = os.path.join(font_folder, fontname)
# font = ImageFont.truetype(fontpath, 20)
font = ImageFont.truetype(fontpath, 24)
font_bold = ImageFont.truetype(fontpath, 26)
font_english = ImageFont.truetype("arial.ttf", 24)
product_font = ImageFont.truetype("arial.ttf", 18)

# Constants for 50mm x 20mm label at 203 DPI
label_width = 400
label_height = 160
combined_width = label_width * 2


def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product=form.save()
            Inventory.objects.get_or_create(product=product)
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
            #generate with text
            # for i in range(0, quantity, 2):
            #     combined_image = Image.new('RGB', (combined_width, label_height), 'white')

            #     for col in range(2):
            #         if i + col >= quantity:
            #             break  # Skip if odd count

            #         barcode_number = product.generate_unique_ean13()
            #         ean = barcode.get('ean13', barcode_number, writer=ImageWriter())
            #         buffer = BytesIO()
            #         ean.write(buffer)
            #         barcode_image = Image.open(buffer)

            #         # Create single label area
            #         label = Image.new('RGB', (label_width, label_height), 'white')
            #         draw = ImageDraw.Draw(label)

            #         # Draw text (adjust Y if needed to fit)
            #         draw.text((5, 5), "lmqfldgqj iy,a", font=font_bold, fill="black")
            #         draw.text((10, 30), f"{product.name}", font=font_english, fill="black")
            #         draw.text((10, 50), f"ñ, • re ¡ {product.price}", font=font, fill="black")
                    

            #         # Resize barcode to fit
            #         barcode_resized = barcode_image.resize((360, 60))
            #         label.paste(barcode_resized, (20, label_height - 65))

            #         # Paste left (col=0) or right (col=1)
            #         x_offset = col * label_width
            #         combined_image.paste(label, (x_offset, 0))

            #     # Save combined label row (2 labels in one image)
            #     filename = f'{product.name}_{i+1:03d}.png'
            #     filepath = os.path.join(product_folder, filename)
            #     combined_image.save(filepath, dpi=(203, 203))
            label_width = 360     # width of each barcode label
            label_height = 160    # height of label (includes barcode + text)
            gap_between_labels = 0  # small gap between the two labels
            combined_width = 2 * label_width - gap_between_labels  # total width for 2 labels
            for i in range(0, quantity, 2):
                combined_image = Image.new('RGB', (combined_width, label_height), 'white')

                for col in range(2):
                    if i + col >= quantity:
                        break

                    barcode_number = product.generate_unique_ean13()
                    ean = barcode.get('ean13', barcode_number, writer=ImageWriter())
                    buffer = BytesIO()
                    ean.write(buffer)
                    barcode_image = Image.open(buffer)

                    # Create label
                    label = Image.new('RGB', (label_width, label_height), 'white')
                    draw = ImageDraw.Draw(label)

                    # Resize barcode to fit inside label
                    barcode_resized = barcode_image.resize((label_width - 10, label_height - 20))
                    label.paste(barcode_resized, (10, 10))

                    # Center text
                    text = product.name
                    text_width = draw.textlength(text, font=product_font)
                    text_x = (label_width - text_width) // 2
                    text_y = label_height - 24

                    draw.text((text_x, text_y), text, font=product_font, fill="black")

                    # Paste label into combined image with reduced gap
                    x_offset = col * (label_width - gap_between_labels)
                    combined_image.paste(label, (x_offset, 0))

                # Save combined image
                filename = f'{product.name}_{i+1:03d}.png'
                filepath = os.path.join(product_folder, filename)
                combined_image.save(filepath, dpi=(203, 203))

            # Generate PDF from barcode images
            pdf_path = os.path.join(product_folder, f"{product.name}_labels.pdf")
            barcode_files = sorted([
                os.path.join(product_folder, f)
                for f in os.listdir(product_folder)
                if f.endswith(".png")
            ])

            # Create PDF: (800x160 px) = ~283 x 57 pt at 72 DPI
            c = canvas.Canvas(pdf_path, pagesize=landscape((283, 57)))

            for img_path in barcode_files:
                c.drawImage(ImageReader(img_path), 0, 0, width=283, height=57)
                c.showPage()

            c.save()

            messages.success(request, f'{quantity} barcode label(s) generated.')

            pdf_url = f"{settings.MEDIA_URL}barcodes/{product.name}/{product.name}_labels.pdf"
            return render(request, 'products/product_detail.html', {
                'product': product,
                'pdf_url': pdf_url
            })

    else:
        form = BarcodeGenerateForm()

    return render(request, 'products/generate_barcodes.html', {'form': form, 'product': product})

def update_stock(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, f"Stock updated for {inventory.product.name}.")
            return redirect('stock_dashboard')
    else:
        form = StockUpdateForm(instance=inventory)

    return render(request, 'inventory/update_stock.html', {
        'inventory': inventory,
        'form': form,
    })

def stock_dashboard(request):
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '')

    inventory_list = Inventory.objects.select_related('product')

    if search_query:
        inventory_list = inventory_list.filter(product__name__icontains=search_query)
    if category_filter:
        inventory_list = inventory_list.filter(product__category=category_filter)

    categories = Product.objects.values_list('category', flat=True).distinct()
    total_stock = inventory_list.aggregate(total=Sum('stock_quantity'))['total']

    return render(request, 'inventory/stock_dashboard.html', {
        'inventory_list': inventory_list,
        'categories': categories,
        'total_stock': total_stock,
    })

