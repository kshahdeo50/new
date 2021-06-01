from django import forms
from django.contrib.auth.models import User
from .models import project
from .models import iam
from .models import rds
from .models import bill

class ProjectForm(forms.ModelForm):
    class Meta:
        model = project
        fields = ['Project_Name','Environment_Name','region','vpc_cidr']
        widgets = {'Project_Name':forms.TextInput(attrs = 
        {'class':'form-control'}),'Environment_Name':forms.TextInput(attrs = 
        {'class':'form-control'}),'region':forms.Select(attrs = 
        {'class':'form-control'}),'vpc_cidr':forms.TextInput(attrs = 
        {'class':'form-control'}),}

class IamForm(forms.ModelForm):
    class Meta:
        model = iam
        fields = ['groupname','username']
        widgets ={'username':forms.TextInput(attrs = 
        {'class':'form-control'}),'groupname':forms.Select(attrs = 
        {'class':'form-control'}),

        }
class RdsForm(forms.ModelForm):
    class Meta:
        model = rds
        fields = ['rds_type','rds_username','rds_password']
        widgets ={'rds_username':forms.TextInput(attrs = 
        {'class':'form-control','placeholder':'Avoid Using "_ -" in username'}), 'rds_password': forms.PasswordInput(attrs = 
        {'class': 'form-control'}),'rds_type':forms.Select(attrs = 
        {'class':'form-control'}),}

class BillForm(forms.ModelForm):
    class Meta:
        model = bill
        fields = ['budget','email']
        widgets = {'email':forms.TextInput(attrs = 
        {'class':'form-control','placeholder':'Get Budget Alerts'}),'budjet':forms.TextInput(attrs = 
        {'class':'form-control','placeholder':'Amount Limit'}),

        }
