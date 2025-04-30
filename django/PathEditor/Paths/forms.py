from django import forms
from .models import Path, Point, Background, UserSelection

class PathForm(forms.ModelForm):
    class Meta:
        model = Path
        fields = ['title']
        widgets = {
            'description': forms.Textarea(attrs={'rows':2}),
        }
        labels = {
            'title': 'Path title'
        }

class PathPointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['x', 'y']
        labels = {
            'x': 'X coordinate',
            'y': 'Y coordinate',
        }
        widgets = {
            'x': forms.NumberInput(attrs={'style': 'width: 80px;', 'min': '0'}),
            'y': forms.NumberInput(attrs={'style': 'width: 80px;', 'min': '0'}),
        }