from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.conf import settings
import os


@staff_member_required
def debug_storage_config(request):
    """
    Debug view to check storage configuration in production.
    Only accessible to staff/admin users.
    """
    config = {
        'IS_RENDER': bool(os.getenv('RENDER')),
        'RENDER_env_var': os.getenv('RENDER', 'NOT SET'),
        'DEBUG': settings.DEBUG,
        'DEFAULT_FILE_STORAGE': getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET'),
        'STORAGES': getattr(settings, 'STORAGES', 'NOT SET'),
        'default_storage_class': default_storage.__class__.__name__,
        'default_storage_module': default_storage.__class__.__module__,
        'CLOUDINARY_CLOUD_NAME': bool(getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)),
        'CLOUDINARY_API_KEY': bool(getattr(settings, 'CLOUDINARY_API_KEY', None)),
        'CLOUDINARY_API_SECRET': bool(getattr(settings, 'CLOUDINARY_API_SECRET', None)),
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_ROOT': str(getattr(settings, 'MEDIA_ROOT', 'NOT SET')),
    }
    
    return JsonResponse(config, json_dumps_params={'indent': 2})
