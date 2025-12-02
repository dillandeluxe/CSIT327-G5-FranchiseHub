import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import Franchise

# Find franchises with missing image files
franchises = Franchise.objects.exclude(image='')
print(f'\n📊 Checking {franchises.count()} franchises with images...\n')

fixed_count = 0
for f in franchises:
    if f.image:
        # Get the full path to the image
        image_path = f.image.path if hasattr(f.image, 'path') else None
        
        if image_path and not os.path.exists(image_path):
            print(f'❌ BROKEN: {f.name}')
            print(f'   Image path: {f.image.name}')
            print(f'   Expected at: {image_path}')
            print(f'   Clearing image field...')
            
            f.image = None
            f.save(update_fields=['image'])
            fixed_count += 1
            print(f'   ✅ Fixed!\n')
        else:
            print(f'✅ OK: {f.name} - Image exists')

print(f'\n🎉 Fixed {fixed_count} franchise(s) with broken image references')
