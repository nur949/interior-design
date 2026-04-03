from django import forms
from .models import Comment, BlogPost, Category, Tag

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']
        widgets = {k: forms.TextInput(attrs={'class':'form-control'}) for k in ['name']}
        widgets.update({'email': forms.EmailInput(attrs={'class':'form-control'}), 'message': forms.Textarea(attrs={'class':'form-control','rows':4})})

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','slug','excerpt','content','category','tags','featured_image','published','featured','meta_description','read_time','published_at']
        widgets = {'content': forms.Textarea(attrs={'rows':12,'class':'form-control'}), 'excerpt': forms.Textarea(attrs={'rows':4,'class':'form-control'}), 'published_at': forms.DateInput(attrs={'type':'date','class':'form-control'})}
