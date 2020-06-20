from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models  import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='email')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate_email(self):
        email = self.cleaned_data.get('email')
        user  = User.objects.filter(email = email).exists()
        if user:
            raise forms.ValidationError('email already taken.')
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='email')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None

    class Meta:
        model  = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['avatar',]
