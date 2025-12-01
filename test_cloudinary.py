"""
Quick test to verify Cloudinary upload is working.
Run with: python manage.py shell < test_cloudinary.py
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Franchise, Franchisor
from django.contrib.auth.models import User

# Create test image
test_image = SimpleUploadedFile(
    name='test_franchise.jpg',
    content=b'fake_image_content',
    content_type='image/jpeg'
)

# Get a franchisor (or create one)
try:
    user = User.objects.filter(franchisor__isnull=False).first()
    if not user:
        print("❌ No franchisor found. Create one first.")
    else:
        franchisor = user.franchisor_set.first()
        
        # Create test franchise
        franchise = Franchise.objects.create(
            franchisor=franchisor,
            name="Test Cloudinary Franchise",
            category="Food & Beverage",
            investment=500000,
            description="Testing Cloudinary upload",
            image=test_image,
            status='pending'
        )
        
        print(f"✅ Franchise created successfully!")
        print(f"📸 Image URL: {franchise.image.url}")
        print(f"☁️ Cloudinary URL: {franchise.image.url}")
        
        # Cleanup
        franchise.delete()
        print("✅ Test franchise deleted")
        
except Exception as e:
    print(f"❌ Error: {e}")
