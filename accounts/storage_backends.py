"""
Custom Django storage backends for different file types.
"""
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def get_document_storage():
    """
    Return appropriate storage backend for documents.
    In production with Supabase: Use SupabaseStorage
    Otherwise: Use FileSystemStorage
    """
    is_render = bool(os.getenv('RENDER'))
    has_supabase = bool(os.getenv('SUPABASE_URL')) and bool(os.getenv('SUPABASE_KEY'))
    
    if is_render and has_supabase:
        try:
            from accounts.supabase_storage import SupabaseStorage
            return SupabaseStorage()
        except Exception as e:
            print(f"⚠️ Failed to initialize Supabase Storage: {e}")
            print(f"⚠️ Falling back to FileSystemStorage")
            return FileSystemStorage()
    else:
        return FileSystemStorage()


# Create a singleton instance
document_storage = get_document_storage()
