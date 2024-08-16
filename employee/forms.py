from django import forms

from employee.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['eid', 'ename', 'eemail', 'econtact', 'prof_image']
        #fields = "__all__"

        widgets = {
            'eid': forms.TextInput(attrs={'class': 'form-control'}),
            'ename': forms.TextInput(attrs={'class': 'form-control'}),
            'eemail': forms.EmailInput(attrs={'class': 'form-control'}),
            'econtact': forms.TextInput(attrs={'class': 'form-control'}),
            'prof_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
