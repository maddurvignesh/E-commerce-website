import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

if os.environ.get('VERCEL'):
    import django
    django.setup()
    from django.core.management import call_command
    from django.db import connection
    tables = connection.introspection.table_names()
    if not tables:
        call_command('migrate', verbosity=0, interactive=False)
        from store.management.commands.seed_data import Command as SeedCmd
        SeedCmd().handle()
        from store.models import Product
        if Product.objects.exists():
            from store.management.commands.add_images import Command as ImgCmd
            try:
                ImgCmd().handle()
            except Exception:
                pass

application = get_wsgi_application()
