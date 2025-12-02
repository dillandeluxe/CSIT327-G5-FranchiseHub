"""
Management command to fix franchises with broken image references.
Clears image fields for franchises where the image file doesn't exist.
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from accounts.models import Franchise
import os


class Command(BaseCommand):
    help = 'Fix franchises with broken image references by clearing non-existent image fields'

    def handle(self, *args, **options):
        self.stdout.write('\n📊 Checking franchises with images...\n')
        
        franchises = Franchise.objects.exclude(image='')
        total = franchises.count()
        fixed_count = 0
        
        self.stdout.write(f'Found {total} franchise(s) with images\n')
        
        for franchise in franchises:
            if franchise.image:
                try:
                    # Try to check if file exists using storage backend
                    if hasattr(default_storage, 'exists'):
                        exists = default_storage.exists(franchise.image.name)
                    else:
                        # For Cloudinary or other backends, assume it exists if we can't check
                        exists = True
                    
                    if not exists:
                        self.stdout.write(self.style.ERROR(f'❌ BROKEN: {franchise.name}'))
                        self.stdout.write(f'   Image path: {franchise.image.name}')
                        self.stdout.write(f'   Clearing image field...')
                        
                        franchise.image = None
                        franchise.save(update_fields=['image'])
                        fixed_count += 1
                        self.stdout.write(self.style.SUCCESS('   ✅ Fixed!\n'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'✅ OK: {franchise.name}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠️  Could not check {franchise.name}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Fixed {fixed_count} franchise(s) with broken image references'))
