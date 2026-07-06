import urllib.request
import ssl
import os
from django.core.files import File
from django.core.management.base import BaseCommand
from store.models import Product
from django.conf import settings


class Command(BaseCommand):
    help = 'Download product-specific images from free stock photo sources'

    def handle(self, *args, **kwargs):
        product_keywords = {
            'Wireless Headphones': 'headphones',
            'Smart Watch': 'smartwatch',
            'Bluetooth Speaker': 'bluetooth,speaker',
            'Laptop Stand': 'laptop,stand',
            'USB-C Hub': 'usb,hub',
            'Mechanical Keyboard': 'keyboard',
            'Classic Hoodie': 'hoodie',
        }

        ctx = ssl._create_unverified_context()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        products = Product.objects.all()
        for product in products:
            kw = product_keywords.get(product.name, f'product{product.pk}')
            downloaded = False

            sources = [
                f'https://loremflickr.com/400/400/{kw}',
                f'https://picsum.photos/seed/{kw.replace(",","-")}/400/400',
            ]

            for url in sources:
                try:
                    req = urllib.request.Request(url, headers=headers)
                    data = urllib.request.urlopen(req, timeout=15, context=ctx).read()
                    if len(data) < 1000:
                        continue
                    path = os.path.join(settings.MEDIA_ROOT, 'products', f'product_{product.pk}.jpg')
                    with open(path, 'wb') as f:
                        f.write(data)
                    with open(path, 'rb') as f:
                        product.image.save(f'product_{product.pk}.jpg', File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'{product.name} ({len(data)} bytes)'))
                    downloaded = True
                    break
                except Exception:
                    continue

            if not downloaded:
                self.stdout.write(self.style.ERROR(f'Failed: {product.name}'))
