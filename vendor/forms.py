from django import forms
from .models import User,Vendor
from accounts.error_printscr import print_message

class VendorRegistrationForm(forms.ModelForm):
  class Meta():
    model = Vendor
    fields =['vendor_name','vendor_license']
