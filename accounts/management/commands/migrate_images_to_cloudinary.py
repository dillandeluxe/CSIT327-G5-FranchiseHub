"""
Management command to migrate existing local images to Cloudinary.
Usage: python manage.py migrate_images_to_cloudinary
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from accounts.models import Franchise, Profile
import os
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Migrate existing local images to Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting image migration to Cloudinary...'))
        
        franchise_count = 0
        profile_count = 0
        errors = []

        # Migrate Franchise images
        self.stdout.write('Migrating franchise images...')
        for franchise in Franchise.objects.exclude(image=''):
            if franchise.image:
                try:
                    # Check if already on Cloudinary
                    if 'cloudinary' in franchise.image.url:
                        self.stdout.write(f'  ✓ {franchise.name} - Already on Cloudinary')
                        continue
                    
                    # Get the file path
                    image_path = franchise.image.path
                    
                    # Check if file exists locally
                    if os.path.exists(image_path):
                        # Read file content
                        with open(image_path, 'rb') as f:
                            file_content = f.read()
                        
                        # Save to Cloudinary (Django will handle the upload)
                        file_name = os.path.basename(image_path)
                        franchise.image.save(file_name, ContentFile(file_content), save=True)
                        
                        franchise_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ {franchise.name} - Migrated'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  ⚠ {franchise.name} - File not found locally'))
                        
                except Exception as e:
                    error_msg = f'{franchise.name}: {str(e)}'
                    errors.append(error_msg)
                    self.stdout.write(self.style.ERROR(f'  ✗ {error_msg}'))

        # Migrate Profile pictures
        self.stdout.write('\nMigrating profile pictures...')
        for profile in Profile.objects.exclude(profile_picture=''):
            if profile.profile_picture:
                try:
                    # Check if already on Cloudinary
                    if 'cloudinary' in profile.profile_picture.url:
                        self.stdout.write(f'  ✓ {profile.user.username} - Already on Cloudinary')
                        continue
                    
                    # Get the file path
                    image_path = profile.profile_picture.path
                    
                    # Check if file exists locally
                    if os.path.exists(image_path):
                        # Read file content
                        with open(image_path, 'rb') as f:
                            file_content = f.read()
                        
                        # Save to Cloudinary
                        file_name = os.path.basename(image_path)
                        profile.profile_picture.save(file_name, ContentFile(file_content), save=True)
                        
                        profile_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ {profile.user.username} - Migrated'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  ⚠ {profile.user.username} - File not found locally'))
                        
                except Exception as e:
                    error_msg = f'{profile.user.username}: {str(e)}'
                    errors.append(error_msg)
                    self.stdout.write(self.style.ERROR(f'  ✗ {error_msg}'))

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Migration complete!'))
        self.stdout.write(f'Franchises migrated: {franchise_count}')
        self.stdout.write(f'Profiles migrated: {profile_count}')
        
        if errors:
            self.stdout.write(self.style.ERROR(f'\nErrors encountered: {len(errors)}'))
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
