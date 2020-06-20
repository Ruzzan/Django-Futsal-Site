from django import forms
from .models import Futsal

class FutsalUpdateForm(forms.ModelForm):
    class Meta:
        model = Futsal
        fields = ['name', 'location', 'main_img', 'cover_img', 'description', 'price']


