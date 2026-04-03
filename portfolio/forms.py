from django import forms
from .models import PortfolioProject

class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = '__all__'
        widgets = {
            'summary': forms.Textarea(attrs={'rows':4,'class':'form-control'}),
            'challenge': forms.Textarea(attrs={'rows':5,'class':'form-control'}),
            'solution': forms.Textarea(attrs={'rows':5,'class':'form-control'}),
            'result': forms.Textarea(attrs={'rows':5,'class':'form-control'}),
            'completed_on': forms.DateInput(attrs={'type':'date','class':'form-control'})
        }
