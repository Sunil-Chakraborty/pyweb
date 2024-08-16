from django import forms
from .models import Directory, File

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter directory name', 'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'owner', 'file', 'url', 'directory']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter file / URL name', 'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'placeholder': 'Owner of the file', 'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'placeholder': 'Select a file', 'class': 'form-control-file'}),
            'url': forms.URLInput(attrs={'placeholder': 'Enter file URL', 'class': 'form-control'}),
            'directory': forms.Select(attrs={'class': 'form-control'}),
        }
