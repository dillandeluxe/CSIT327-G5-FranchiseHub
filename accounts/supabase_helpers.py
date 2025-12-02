"""
Helper functions to manually upload documents to Supabase Storage
after Django saves them to default storage.
"""
import os
from accounts.storage_backends import document_storage


def upload_to_supabase(file_field):
    """
    Manually upload a file to Supabase Storage if configured.
    This is called after Django saves the file to local/Cloudinary storage.
    
    Args:
        file_field: Django FileField or ImageField instance
        
    Returns:
        Updated URL if uploaded to Supabase, otherwise original URL
    """
    if not file_field:
        return None
    
    # Check if we should use Supabase (only for documents, not images)
    is_render = bool(os.getenv('RENDER'))
    has_supabase = bool(os.getenv('SUPABASE_URL')) and bool(os.getenv('SUPABASE_KEY'))
    
    if not (is_render and has_supabase):
        return file_field.url  # Return original URL
    
    # Check if this is a document (not an image)
    file_path = file_field.name
    if not any(ext in file_path.lower() for ext in ['.pdf', '.doc', '.docx', '.txt']):
        return file_field.url  # Return original URL for images
    
    try:
        from accounts.supabase_storage import SupabaseStorage
        supabase_storage = SupabaseStorage()
        
        # Read file content
        file_field.open('rb')
        content = file_field.read()
        file_field.close()
        
        # Upload to Supabase
        supabase_storage._save(file_path, content)
        
        # Get Supabase URL
        supabase_url = supabase_storage.url(file_path)
        print(f"✅ Uploaded to Supabase: {file_path} -> {supabase_url}")
        
        return supabase_url
        
    except Exception as e:
        print(f"⚠️ Failed to upload to Supabase: {e}")
        return file_field.url  # Return original URL on error
