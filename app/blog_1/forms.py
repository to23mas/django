from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Zadejte název příspěvku'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                'rows': 5,
                'placeholder': 'Napište obsah příspěvku...'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2 m-4'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        error_css_class = "error"
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Zadejte název kategorie'
            }),
        }
        error_messages = {
            'name': {
                'unique': 'Tento název kategorie již existuje.'
            }
        }
