"""
Custom Django storage backend for Supabase Storage.
Handles file uploads to Supabase Storage buckets.
"""
import os
from io import BytesIO
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from supabase import create_client, Client
from urllib.parse import urljoin


@deconstructible
class SupabaseStorage(Storage):
    """
    Custom storage backend for Supabase Storage.
    Uploads files to Supabase and generates public URLs.
    """
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.bucket_name = os.getenv('SUPABASE_BUCKET', 'franchise-documents')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def _save(self, name, content):
        """
        Save file to Supabase Storage.
        """
        # Read file content
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content
        
        # Upload to Supabase Storage
        try:
            response = self.client.storage.from_(self.bucket_name).upload(
                path=name,
                file=file_content,
                file_options={"content-type": self._get_content_type(name)}
            )
            print(f"✅ Uploaded to Supabase Storage: {name}")
            return name
        except Exception as e:
            print(f"❌ Supabase upload error: {e}")
            # If file exists, try updating instead
            try:
                response = self.client.storage.from_(self.bucket_name).update(
                    path=name,
                    file=file_content,
                    file_options={"content-type": self._get_content_type(name)}
                )
                print(f"✅ Updated in Supabase Storage: {name}")
                return name
            except Exception as update_error:
                print(f"❌ Supabase update error: {update_error}")
                raise
    
    def _open(self, name, mode='rb'):
        """
        Download file from Supabase Storage.
        """
        try:
            response = self.client.storage.from_(self.bucket_name).download(name)
            return BytesIO(response)
        except Exception as e:
            print(f"❌ Supabase download error: {e}")
            raise
    
    def exists(self, name):
        """
        Check if file exists in Supabase Storage.
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(name))
            basename = os.path.basename(name)
            return any(f['name'] == basename for f in files)
        except:
            return False
    
    def url(self, name):
        """
        Generate public URL for file.
        """
        try:
            response = self.client.storage.from_(self.bucket_name).get_public_url(name)
            return response
        except Exception as e:
            print(f"❌ Error generating Supabase URL: {e}")
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"
    
    def delete(self, name):
        """
        Delete file from Supabase Storage.
        """
        try:
            self.client.storage.from_(self.bucket_name).remove([name])
            print(f"✅ Deleted from Supabase Storage: {name}")
        except Exception as e:
            print(f"❌ Supabase delete error: {e}")
    
    def size(self, name):
        """
        Get file size.
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(name))
            basename = os.path.basename(name)
            for f in files:
                if f['name'] == basename:
                    return f.get('metadata', {}).get('size', 0)
            return 0
        except:
            return 0
    
    def _get_content_type(self, name):
        """
        Determine content type based on file extension.
        """
        ext = os.path.splitext(name)[1].lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
        }
        return content_types.get(ext, 'application/octet-stream')
