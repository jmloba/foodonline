from django import forms

from .models import Category, Product_Menu
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields=['category_name','description']

class ProductItemForm(forms.ModelForm):
  image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}),validators=[allow_only_images_validator])
  class Meta:
    model = Product_Menu    
    fields=['category','product_itemno', 'product_title','description','cost_price','price', 'image','is_available',]

