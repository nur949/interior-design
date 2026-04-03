from django import forms
from .models import ContactMessage, Subscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','phone','subject','message']
        widgets = {'message': forms.Textarea(attrs={'rows':5,'class':'form-control'})}

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Your email address'})}
