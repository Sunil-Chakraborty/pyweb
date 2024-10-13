# transactions/forms.py

from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['tr', 'name', 'comment', 'amount', 'date']
        widgets = {
            'tr': forms.Select(choices=Transaction.TRANSACTION_TYPES),
            #'tr': widgets.Select(attrs={'style': 'width:250px;height:40px'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),  # Step can be adjusted as 
           
        }
