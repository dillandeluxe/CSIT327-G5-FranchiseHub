import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# This imports the default Django User model (defined by settings.AUTH_USER_MODEL)
# via a Foreign Key to link profiles to users.

class Franchisee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Links this profile to a base Django User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
    business_name = models.TextField()
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # NOTE: managed = False is used because you are likely pointing to pre-existing tables.
        # Ensure this is what you intend, as Django will not create or alter these tables.
        db_table = 'franchisee'
        managed = False

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"


class Franchisor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Links this profile to a base Django User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
    company_name = models.TextField()
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'franchisor'
        managed = False

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class AdminProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Links this profile to a base Django User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
    full_name = models.TextField()
    role_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_profile'
        managed = False

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

class Profile(models.Model):
    # One-to-one link to the base Django User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
# ----------------------------------------