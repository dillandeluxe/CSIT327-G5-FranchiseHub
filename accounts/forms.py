# accounts/forms.py
from django import forms
from .models import Profile, Franchise

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'location', 'bio', 'profile_picture']

class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ['name', 'category', 'investment', 'description', 'is_active']
