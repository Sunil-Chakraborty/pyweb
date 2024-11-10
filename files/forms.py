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


class PDFPasswordForm(forms.Form):
    pdf_file = forms.FileField(label="Upload PDF")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    


class PDFWatermarkForm(forms.Form):
    pdf_file = forms.FileField(label="Select PDF file")
    watermark_text = forms.CharField(label="Watermark Text", max_length=100)
    


class PDFTextureForm(forms.Form):
    pdf_file = forms.FileField(label="PDF File")
    texture_image = forms.ImageField(label="Texture Image")
    opacity = forms.FloatField(label="Opacity", initial=0.3, min_value=0, max_value=1)
