from django import forms
from .models import Mark

class MarkInputForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class MarkUpdateForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['module_code', 'student_id', 'date', 'cw1', 'cw2', 'cw3']