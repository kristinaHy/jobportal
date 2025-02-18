from django import forms
from .models import UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Application, JobCategory
from django.utils import timezone

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'skills', 'experience', 
                 'resume', 'profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            'title', 'company', 'description', 'requirements', 'benefits',
            'location', 'salary', 'job_type', 'experience_level', 'category',
            'is_active', 'application_deadline'
        ]
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'benefits': forms.Textarea(attrs={'rows': 4}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter', 'notes']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
