from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import random

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    product_code = models.CharField(max_length=4, blank=True)  # New field
    barcode_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True)

    def save(self, *args, **kwargs):
        # Only generate barcode if barcode_number is not set AND a special flag is passed via kwargs
        generate_barcode = kwargs.pop('generate_barcode', False)
        
        if not self.barcode_number and generate_barcode:
            self.barcode_number = self.generate_unique_ean13()
            ean = barcode.get('ean13', self.barcode_number, writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            self.barcode_image.save(f'{self.barcode_number}.png', File(buffer), save=False)
        
        super().save(*args, **kwargs)

    def generate_unique_ean13(self):
        category_code = '200'  # e.g., 200 = rice
        product_code = self.product_code or str(self.id).zfill(4)  # fallback if empty

        while True:
            unique_serial = str(random.randint(0, 99999)).zfill(5)  # Always 5 digits
            base_code = category_code + product_code + unique_serial  # 12 digits

            # EAN13 checksum calculation
            digits = [int(d) for d in base_code]
            odd_sum = sum(digits[::2])
            even_sum = sum(digits[1::2])
            total = odd_sum + even_sum * 3
            check_digit = (10 - (total % 10)) % 10

            full_code = base_code + str(check_digit)  # 13-digit EAN13

            # Check uniqueness
            if not Product.objects.filter(barcode_number=full_code).exists():
                return full_code


    def __str__(self):
        return f"{self.name} ({self.barcode_number})"