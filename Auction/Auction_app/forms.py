# forms.py
from django import forms
from Auction_app.models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['heading', 'description', 'image']
