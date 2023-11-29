from django import forms

from .models import Employee, Team

class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'

class TeamForm(forms.ModelForm):
    class Meta:
        model=Team
        fields='__all__'