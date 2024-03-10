from django import forms
from .models import User
from .error_printscr import print_message


class UserForm(forms.ModelForm):
  password         = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields=[
      'first_name',
      'last_name',
      'username',
      'email',
      'password'
    ]

  def clean(self):
    cleaned_data = super(UserForm,self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    if password != confirm_password:
      mess = f'password does not match ------->:{password} / {confirm_password}'
      print_message(mess)

      raise forms.ValidationError('Password does not match')
  