from django import forms
from .models import FurnitureItem

class FurnitureItemForm(forms.ModelForm):
    class Meta:
        model = FurnitureItem
        fields = '__all__'
        widgets = {'description': forms.Textarea(attrs={'rows':8, 'class':'form-control'})}
