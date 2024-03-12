from django import forms
from .models import User,Vendor
from accounts.error_printscr import print_message
from accounts.validators import allow_only_images_validator

class VendorRegistrationForm(forms.ModelForm):
  vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])  
  class Meta():
    model = Vendor
    fields =['vendor_name','vendor_license']


