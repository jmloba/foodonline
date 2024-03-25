

from django import forms
from .models import InvoiceMaster
from orm_module.models import Student

from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.db import models

class InvoiceMasterForm(forms.ModelForm):
  invoice_no = forms.IntegerField()
    
  class Meta:
    model = InvoiceMaster
    fields =['invoice_no','invoice_desc']


def  name_starts_with_G(value)  :
  if value[0] != 'G':
    raise forms.ValidationError('This shoud starts with G')


    
class Student_form(forms.ModelForm):
  firstname= forms.CharField(validators=[name_starts_with_G,MinLengthValidator(4), MaxLengthValidator(25)])
  lastname= forms.CharField(validators=[MinLengthValidator(4), MaxLengthValidator(25)])
  email=forms.EmailField()
  class Meta:
    model =Student
    fields=['firstname','lastname', 'email', 'age','classroom' ]
  

    
