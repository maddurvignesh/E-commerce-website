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
        call_command('seed_data', verbosity=0)
        from store.models import Product
        from django.core.files import File as DjangoFile
        import glob
        for path in sorted(glob.glob('/var/task/media/products/product_*.jpg')):
            fname = os.path.basename(path)
            parts = fname.split('_')
            try:
                pid = int(parts[1])
            except (IndexError, ValueError):
                continue
            try:
                prod = Product.objects.get(pk=pid)
            except Product.DoesNotExist:
                continue
            if not prod.image:
                with open(path, 'rb') as f:
                    prod.image.save(fname, DjangoFile(f), save=True)

application = get_wsgi_application()
