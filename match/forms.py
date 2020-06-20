from django import forms
from .models import Match

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class MatchForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput,help_text='user hour-minute- AM/PM')
    end_time = forms.TimeField(widget=TimeInput,help_text='user hour-minute- AM/PM')
    class Meta:
        model = Match
        fields = [
            'team',
            'futsal',
            'date',
            'start_time',
            'end_time',
            'player_count',
            'game_type'
        ]
        exclude = ('team',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control my-1'
    