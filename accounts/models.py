import uuid  # ✅ ADD missing import
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.utils import timezone
from accounts.storage_backends import document_storage

# This imports the default Django User model (defined by settings.AUTH_USER_MODEL)
# via a Foreign Key to link profiles to users.

# =========================
#  FRANCHISEE MODEL
# =========================
class Franchisee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    db_column='user_id',
    null=True,      # ✅ allow empty temporarily so migration won't fail
    blank=True      # ✅ allow forms to save without user (for now)
)
    business_name = models.TextField()
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'franchisee'
        managed = True  # ✅ Django will create and manage this table

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"


# =========================
#  FRANCHISOR MODEL
# =========================
class Franchisor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    db_column='user_id',
    null=True,      # ✅ allow temporarily null so migrations won't fail
    blank=True      # ✅ allow form entries without user for now
)
    company_name = models.TextField()
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    location = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text="City, State/Province, Country (e.g., Manila, Philippines)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'franchisor'
        managed = True  # ✅ let Django handle table creation

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


# =========================
#  ADMIN PROFILE MODEL
# =========================
class AdminProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        null=True,      # ✅ allow temporarily null
        blank=True      # ✅ allow form submission without user
    )
    full_name = models.TextField()
    role_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_profile'
        managed = True

    def __str__(self):
        return f"{self.full_name} ({self.user.username if self.user else 'No user'})"



# =========================
#  FRANCHISE MODEL (UPDATED)
# =========================
class Franchise(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    franchisor = models.ForeignKey(Franchisor, on_delete=models.CASCADE, related_name='franchises')
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    investment = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='franchise_images/', blank=True, null=True)
    
    # ✅ ADDED BACK: Document fields for file uploads
    brochure = models.FileField(
        upload_to='franchise_documents/', 
        storage=lambda: document_storage,
        blank=True, 
        null=True,
        help_text="Upload franchise brochure (PDF, DOC, DOCX, etc.)",
        max_length=500
    )
    business_plan = models.FileField(
        upload_to='franchise_documents/', 
        storage=lambda: document_storage,
        blank=True, 
        null=True,
        help_text="Upload business plan document (PDF, DOC, DOCX, etc.)",
        max_length=500
    )
    
    # ✅ NEW STATUS FIELDS
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)  # For soft delete
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_franchises'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'franchise'
        managed = True
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def formatted_investment(self):
        """Format investment amount with currency symbol"""
        if self.investment:
            return f"₱{self.investment:,.0f}"
        return "₱0"

    @property
    def short_description(self):
        """Return shortened description for cards"""
        if self.description and len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description or "No description available."
    
    def approve(self, admin_user):
        """Approve franchise and create notification"""
        self.status = 'approved'
        self.reviewed_at = timezone.now()
        self.reviewed_by = admin_user
        self.save(update_fields=['status', 'reviewed_at', 'reviewed_by'])
        
        # Create notification
        Notification.objects.create(
            user=self.franchisor.user,
            title='Franchise Approved! 🎉',
            message=f'Your franchise "{self.name}" has been approved and is now live on the platform!',
            notification_type='approval',
            related_franchise=self
        )
    
    def reject(self, admin_user, reason=''):
        """Reject franchise and create notification"""
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.reviewed_by = admin_user
        self.rejection_reason = reason
        self.save(update_fields=['status', 'reviewed_at', 'reviewed_by', 'rejection_reason'])
        
        # Create notification
        Notification.objects.create(
            user=self.franchisor.user,
            title='Franchise Review Update',
            message=f'Your franchise request for "{self.name}" was not approved. {reason}',
            notification_type='rejection',
            related_franchise=self
        )

# =========================
#  NOTIFICATION MODEL (NEW)
# =========================
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('approval', 'Approval'),
        ('rejection', 'Rejection'),
        ('general', 'General'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    related_franchise = models.ForeignKey(
        Franchise,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notification'
        managed = True
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

# =========================
#  PROFILE MODEL
# =========================
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    class Meta:
        db_table = 'profile'
        managed = True

    def __str__(self):
        return self.full_name or self.user.username

# =========================
#  SECURITY QUESTION MODEL
# =========================
class SecurityQuestion(models.Model):
    """
    Stores user's security questions and hashed answers for password recovery.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='security_questions'
    )
    question_1 = models.CharField(max_length=255, default="What is the name of your childhood best friend?")
    answer_1_hash = models.CharField(max_length=255)  # Hashed answer
    
    question_2 = models.CharField(max_length=255, default="What city were you born in?")
    answer_2_hash = models.CharField(max_length=255)  # Hashed answer
    
    question_3 = models.CharField(max_length=255, default="What was the name of your first pet?")
    answer_3_hash = models.CharField(max_length=255)  # Hashed answer
    
    failed_attempts = models.IntegerField(default=0)  # Track failed recovery attempts
    locked_until = models.DateTimeField(null=True, blank=True)  # Temporary lockout
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'security_questions'
        managed = True

    def __str__(self):
        return f"Security Questions for {self.user.username}"

    def set_answer(self, question_num, answer):
        """Hash and store answer (1, 2, or 3)"""
        normalized = answer.strip().lower()
        hashed = make_password(normalized)
        if question_num == 1:
            self.answer_1_hash = hashed
        elif question_num == 2:
            self.answer_2_hash = hashed
        elif question_num == 3:
            self.answer_3_hash = hashed

    def check_answer(self, question_num, answer):
        """Verify answer (case-insensitive, trimmed)"""
        normalized = answer.strip().lower()
        if question_num == 1:
            return django_check_password(normalized, self.answer_1_hash)
        elif question_num == 2:
            return django_check_password(normalized, self.answer_2_hash)
        elif question_num == 3:
            return django_check_password(normalized, self.answer_3_hash)
        return False

    def check_all_answers(self, answer1, answer2, answer3):
        """Verify all three answers at once"""
        return (
            self.check_answer(1, answer1) and
            self.check_answer(2, answer2) and
            self.check_answer(3, answer3)
        )

    def record_failed_attempt(self):
        """Increment failed attempts and lock if threshold reached"""
        from django.utils import timezone
        from datetime import timedelta
        
        self.failed_attempts += 1
        if self.failed_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(hours=1)
        self.save(update_fields=['failed_attempts', 'locked_until'])

    def reset_failed_attempts(self):
        """Clear failed attempts after successful recovery"""
        self.failed_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_attempts', 'locked_until'])

    def is_locked(self):
        """Check if account is temporarily locked"""
        from django.utils import timezone
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

# =========================
#  FRANCHISE APPLICATION MODEL (MISSING - NOW ADDED)
# =========================
class FranchiseApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    franchisee = models.ForeignKey(
        Franchisee,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    # Applicant Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    experience = models.TextField(blank=True, null=True, help_text="Business experience and background")
    
    # ✅ Document upload fields
    resume = models.FileField(
        upload_to='application_documents/',
        storage=lambda: document_storage,
        blank=True,
        null=True,
        help_text="Upload your resume/CV (PDF, DOC, DOCX)",
        max_length=500
    )
    business_proposal = models.FileField(
        upload_to='application_documents/',
        storage=lambda: document_storage,
        blank=True,
        null=True,
        help_text="Upload your business proposal (PDF, DOC, DOCX)",
        max_length=500
    )
    financial_statement = models.FileField(
        upload_to='application_documents/',
        storage=lambda: document_storage,
        blank=True,
        null=True,
        help_text="Upload financial statement or proof of funds (PDF)",
        max_length=500
    )
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approval_note = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'franchise_application'
        managed = True
        ordering = ['-created_at']
        verbose_name = 'Franchise Application'
        verbose_name_plural = 'Franchise Applications'
    
    def __str__(self):
        return f"{self.full_name} - {self.franchise.name} ({self.status})"
    
    def approve(self):
        """Approve application"""
        self.status = 'Approved'
        self.save()
    
    def reject(self):
        """Reject application"""
        self.status = 'Rejected'
        self.save()

# =========================
#  USER FAVORITES MODEL (NEW)
# =========================
class UserFavorites(models.Model):
    """
    Stores franchises that users have favorited/bookmarked.
    Each user can favorite multiple franchises.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_favorites'
        managed = True
        unique_together = ('user', 'franchise')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.franchise.name}"

