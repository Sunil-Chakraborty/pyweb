from django import forms
from .models import Recepi, Compound, RawMat, MixProd

class RecepiForm(forms.ModelForm):

    

    class Meta:
        model = Recepi
        comp_cd = forms.ModelChoiceField(queryset=Compound.objects.all(), label="Compound")
        rm_cd = forms.ModelChoiceField(queryset=RawMat.objects.all(), label="Raw Material")

        fields = ['card_no','doc_dt','comp_cd', 'rm_cd', 'qty']
        widgets = {
            'comp_cd': forms.Select(attrs={'class': 'form-control'}),
            'rm_cd': forms.Select(attrs={'class': 'form-control'}),            
            'qty': forms.NumberInput(attrs={'class': 'form-control'}),
        }
     
        
class MixProdForm(forms.ModelForm):
    class Meta:
        model = MixProd
        fields = ['card_no', 'prod_no', 'prod_dt', 'qty']  # Ensure all fields are included
