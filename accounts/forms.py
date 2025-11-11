from django import forms
from .models import Profile, Franchise, FranchiseApplication

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'location', 'bio', 'profile_picture']

class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ['name', 'category', 'investment', 'description']

class FranchiseApplicationForm(forms.ModelForm):
    """Franchisee-facing application form (franchise & franchisee set in view)."""
    class Meta:
        model = FranchiseApplication
        fields = ['full_name', 'email', 'phone', 'experience']
        widgets = {
            'experience': forms.Textarea(attrs={'rows': 3})
        }
