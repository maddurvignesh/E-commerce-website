from django.core.management.base import BaseCommand
from store.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': 'Wireless Headphones',
                'description': 'High-quality wireless headphones with noise cancellation, 30-hour battery life, and premium sound quality. Perfect for music lovers and professionals.',
                'price': Decimal('79.99'),
                'stock': 25,
            },
            {
                'name': 'Smart Watch',
                'description': 'Feature-packed smartwatch with heart rate monitoring, GPS tracking, sleep analysis, and a vibrant AMOLED display. Compatible with iOS and Android.',
                'price': Decimal('199.99'),
                'stock': 15,
            },
            {
                'name': 'Bluetooth Speaker',
                'description': 'Portable Bluetooth speaker with deep bass, 360-degree sound, IPX7 waterproof rating, and 12-hour playtime. Take your music anywhere.',
                'price': Decimal('49.99'),
                'stock': 40,
            },
            {
                'name': 'Laptop Stand',
                'description': 'Ergonomic aluminum laptop stand with adjustable height, ventilated design for heat dissipation, and foldable construction for portability.',
                'price': Decimal('34.99'),
                'stock': 50,
            },
            {
                'name': 'USB-C Hub',
                'description': '7-in-1 USB-C hub with HDMI 4K output, 2 USB 3.0 ports, SD/TF card reader, and 100W Power Delivery pass-through charging.',
                'price': Decimal('44.99'),
                'stock': 35,
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'RGB mechanical keyboard with hot-swappable switches, PBT keycaps, and a compact 75% layout. Built for typists and gamers alike.',
                'price': Decimal('89.99'),
                'stock': 20,
            },
            {
                'name': 'Classic Hoodie',
                'description': 'Comfortable cotton-blend hoodie with a modern fit. Features a kangaroo pocket, adjustable drawstring hood, and ribbed cuffs. Perfect for casual wear.',
                'price': Decimal('59.99'),
                'stock': 30,
            },
        ]

        for data in products:
            Product.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(products)} products'))
