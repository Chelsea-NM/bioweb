from django import forms
from .models import proteins


class ProteinsForm(forms.ModelForm):
    class Meta:
        model = proteins
        fields = ['proteinID', 'sequence']
