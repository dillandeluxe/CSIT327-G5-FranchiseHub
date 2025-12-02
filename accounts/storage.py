"""
Storage backend utilities for FranchiseHub.
This module provides a function to get the correct storage backend based on environment.
"""

import os
from django.core.files.storage import FileSystemStorage


def get_storage():
    """
    Get the appropriate storage backend based on environment.
    
    Returns:
        Storage backend instance (MediaCloudinaryStorage or FileSystemStorage)
    """
    IS_RENDER = os.getenv('RENDER', '').lower() == 'true'
    
    if IS_RENDER:
        # Production: Use Cloudinary
        from cloudinary_storage.storage import MediaCloudinaryStorage
        return MediaCloudinaryStorage()
    else:
        # Development: Use local filesystem
        return FileSystemStorage()
