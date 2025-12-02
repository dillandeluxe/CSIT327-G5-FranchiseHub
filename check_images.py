import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import Franchise

franchises = Franchise.objects.all()
print(f'\n📊 Total franchises: {franchises.count()}\n')

for f in franchises[:10]:
    image_path = f.image.name if f.image else 'None'
    print(f'ID: {f.id}')
    print(f'  Name: {f.name}')
    print(f'  Image: {image_path}')
    if f.image:
        print(f'  URL: {f.image.url}')
    print()
