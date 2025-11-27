from django import forms
from .models import Profile, Franchise, FranchiseApplication

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'location', 'bio', 'profile_picture']

class FranchiseForm(forms.ModelForm):
    """Form for creating and editing franchises"""
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
                'placeholder': 'Minimum investment amount',
                'step': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'placeholder': 'Describe your franchise opportunity...',
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
    """Form for franchisee applications"""
    class Meta:
        model = FranchiseApplication
        fields = ['full_name', 'email', 'phone', 'experience']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your business experience...',
                'rows': 4
            })
        }
