from django import forms
from .models import Booking

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BookingForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput,help_text='user hour-minute- AM/PM')
    class Meta:
        model = Booking
        fields = [
            'fullname',
            'phone',
            'date',
            'time',
        ]

class CreateBookingForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateInput(attrs={'class':'form-control'}))
    time = forms.TimeField(widget=TimeInput, help_text='user hour-minute-AM/PM')
    class Meta:
        model = Booking
        fields = [
            'fullname',
            'phone',
            'futsal',
            'date',
            'time'
        ]

        widgets = {
            'fullname':forms.TextInput(attrs={'class':'form-control mb-2'}),
            'phone':forms.NumberInput(attrs={'class':'form-control mb-2'}),
            'futsal':forms.Select(attrs={'class':'form-control mb-2'}),
        }