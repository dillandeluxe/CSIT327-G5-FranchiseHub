import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password as django_check_password

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
#  FRANCHISE MODEL
# =========================
class Franchise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    franchisor = models.ForeignKey(Franchisor, on_delete=models.CASCADE, related_name='franchises')
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    investment = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='franchise_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'franchise'
        managed = True  # ✅ this is your main “Franchise” table

    def __str__(self):
        return f"{self.name} ({self.franchisor.company_name})"

    # --- New helper properties for display on browse.html (no DB migration needed) ---
    @property
    def formatted_investment(self):
        """
        Returns an investment string close to the static card style.
        Example: '₱450,000+ Investment'
        """
        try:
            value = int(self.investment)
            return f"₱{value:,.0f}+ Investment"
        except Exception:
            return "₱— Investment"

    @property
    def short_description(self):
        """
        Truncates the description to fit the static card box aesthetic.
        """
        text = (self.description or "").strip() or "No description provided."
        return (text[:110] + "…") if len(text) > 110 else text


# =========================
#  FRANCHISE APPLICATION MODEL
# =========================
class FranchiseApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='applications')
    franchisee = models.ForeignKey(Franchisee, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    experience = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        default='Pending',
        choices=[
            ('Pending', 'Pending Review'),
            ('Accepted', 'Accepted'),   # added
            ('Approved', 'Approved'),   # kept for backward compatibility
            ('Rejected', 'Rejected'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # --- New fields ---
    rejection_reason = models.TextField(null=True, blank=True)  # why rejected
    approval_note = models.TextField(null=True, blank=True)     # optional acceptance note

    class Meta:
        db_table = 'franchise_application'
        managed = True  # ✅ managed by Django
        ordering = ['-created_at']  # New: newest first for dashboards

    def __str__(self):
        return f"{self.full_name} → {self.franchise.name}"

    # --- New helper methods for status transitions (convenience, optional) ---
    def approve(self):
        # legacy helper left as-is (sets Approved)
        self.status = 'Approved'
        self.save(update_fields=['status'])

    def reject(self):
        self.status = 'Rejected'
        self.save(update_fields=['status'])


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
        managed = True  # ✅ new table managed by Django

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

