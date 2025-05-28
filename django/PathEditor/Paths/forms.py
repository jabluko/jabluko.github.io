from django import forms
from .models import Path, Point, Background, UserSelection, GameBoard, DotsJSON

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

class BoardForm(forms.ModelForm):
    class Meta:
        model = GameBoard
        fields = ['name', 'rows', 'cols']
        labels = {
            'name': 'Board name',
            'rows': 'Number of rows',
            'cols': 'Number of columns',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Board name'}),
            'rows': forms.NumberInput(attrs={'min': 1, 'style': 'width: 80px;'}),
            'cols': forms.NumberInput(attrs={'min': 1, 'style': 'width: 80px;'}),
        }

class BoardPointsForm(forms.Form):
    points = forms.JSONField(label="JSON of points")
