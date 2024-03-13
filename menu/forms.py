from django import forms

from .models import Category

class CategoryForm(forms.ModelForm):
  # password         = forms.CharField(widget=forms.PasswordInput())
  # confirm_password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = Category
    fields=['category_name','description']

  # def clean(self):
  #   cleaned_data = super(UserForm,self).clean()
  #   password = cleaned_data.get('password')
  #   confirm_password = cleaned_data.get('confirm_password')
  #   if password != confirm_password:
  #     mess = f'password does not match ------->:{password} / {confirm_password}'
  #     print_message(mess)
  #     raise forms.ValidationError('Password does not match')