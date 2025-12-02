"""
Storage backend utilities for FranchiseHub.
This module provides storage backend selection based on environment.
"""

import os
from django.core.files.storage import FileSystemStorage


class DynamicStorage:
    """
    Dynamic storage backend that selects Cloudinary or FileSystem based on environment.
    This is a callable class that Django can use as a storage parameter.
    """
    def __call__(self):
        IS_RENDER = os.getenv('RENDER', '').lower() == 'true'
        
        if IS_RENDER:
            # Production: Use Cloudinary
            from cloudinary_storage.storage import MediaCloudinaryStorage
            return MediaCloudinaryStorage()
        else:
            # Development: Use local filesystem
            return FileSystemStorage()


# Create a singleton instance that can be imported
get_storage = DynamicStorage()
