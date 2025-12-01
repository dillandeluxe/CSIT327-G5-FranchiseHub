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
        fields = ['name', 'category', 'investment', 'description', 'image', 'brochure', 'business_plan']  # ✅ Include documents
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
            # ✅ Document widgets
            'brochure': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'business_plan': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def clean_investment(self):
        investment = self.cleaned_data.get('investment')
        if investment and investment < 0:
            raise forms.ValidationError('Investment amount must be positive')
        return investment
    
    # ✅ Document validation
    def clean_brochure(self):
        brochure = self.cleaned_data.get('brochure')
        if brochure and hasattr(brochure, 'size') and brochure.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size must be less than 10MB')
        return brochure

    def clean_business_plan(self):
        business_plan = self.cleaned_data.get('business_plan')
        if business_plan and hasattr(business_plan, 'size') and business_plan.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size must be less than 10MB')
        return business_plan

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
    class Meta:
        model = FranchiseApplication
        fields = [
            'full_name',
            'email', 
            'phone',
            'experience',  # ✅ Make sure this is included
            'resume',
            'business_proposal',
            'financial_statement'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+63 XXX XXX XXXX',
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your business experience, background, and qualifications...',
                'rows': 5
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'business_proposal': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'financial_statement': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and resume.size > 10 * 1024 * 1024:  # 10MB limit
            raise forms.ValidationError('File size must be less than 10MB')
        return resume

    def clean_business_proposal(self):
        proposal = self.cleaned_data.get('business_proposal')
        if proposal and proposal.size > 10 * 1024 * 1024:  # 10MB limit
            raise forms.ValidationError('File size must be less than 10MB')
        return proposal

    def clean_financial_statement(self):
        statement = self.cleaned_data.get('financial_statement')
        if statement and statement.size > 10 * 1024 * 1024:  # 10MB limit
            raise forms.ValidationError('File size must be less than 10MB')
        return statement
