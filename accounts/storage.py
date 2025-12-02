"""
Storage backend utilities for FranchiseHub.
This module provides storage backend selection based on environment.
"""

import os
from django.core.files.storage import FileSystemStorage


def select_storage():
    """
    Returns the appropriate storage instance based on environment.
    This function is called by Django when initializing file fields.
    """
    IS_RENDER = os.getenv('RENDER', '').lower() == 'true'
    
    if IS_RENDER:
        # Production: Use Cloudinary
        from cloudinary_storage.storage import MediaCloudinaryStorage
        return MediaCloudinaryStorage()
    else:
        # Development: Use local filesystem
        return FileSystemStorage()
