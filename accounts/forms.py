from django import forms
from .models import Profile, Franchise, FranchiseApplication

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'location', 'bio', 'profile_picture']

class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ['name', 'category', 'investment', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter franchise name'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Food & Beverage, Retail, Services'
            }),
            'investment': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum investment required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'placeholder': 'Provide a detailed description of your franchise...',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'name': 'Franchise Name',
            'category': 'Category/Industry',
            'investment': 'Minimum Investment (₱)',
            'description': 'Description',
            'image': 'Franchise Image/Logo'
        }

class FranchiseApplicationForm(forms.ModelForm):
    """Franchisee-facing application form (franchise & franchisee set in view)."""
    class Meta:
        model = FranchiseApplication
        fields = ['full_name', 'email', 'phone', 'experience']
        widgets = {
            'experience': forms.Textarea(attrs={'rows': 3})
        }
