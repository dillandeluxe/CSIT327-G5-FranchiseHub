from django import forms
from .models import Profile, Franchise, FranchiseApplication, Franchisor  # ✅ ADD Franchisor import

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'location', 'bio', 'profile_picture']

class FranchiseForm(forms.ModelForm):
    """Form for creating and editing franchises"""
    class Meta:
        model = Franchise
        fields = ['name', 'category', 'investment', 'description', 'image']  # ✅ Removed brochure and business_plan
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter franchise name',
                'required': True
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Food & Beverage, Retail',
                'required': True
            }),
            'investment': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum investment amount',
                'required': True,
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
            }),
        }

    def clean_investment(self):
        investment = self.cleaned_data.get('investment')
        if investment and investment < 0:
            raise forms.ValidationError('Investment amount must be positive')
        return investment

# ✅ NEW: Franchisor Form with Location
class FranchisorForm(forms.ModelForm):
    class Meta:
        model = Franchisor  # ✅ Now this will work since Franchisor is imported
        fields = ['company_name', 'email', 'phone', 'country', 'location']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'company@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 234 567 8900'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Philippines, United States'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control location-input',
                'placeholder': 'e.g., Manila, Philippines or New York, NY, USA'
            })
        }
    
    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location and len(location.strip()) < 2:
            raise forms.ValidationError("Location must be at least 2 characters long.")
        return location

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
