from django.db import models
from vendor.models import Vendor

# Create your models here.

class Category(models.Model):
  vendor        = models.ForeignKey(Vendor,on_delete=models.CASCADE)
  category_name = models.CharField(max_length= 50) #ex seafood -> sea-food
  slug          = models.SlugField(max_length=50, unique=True)
  description   = models.TextField(max_length=250, unique=True)
  created_at    = models.DateTimeField(auto_now_add=True)
  updated_at    = models.DateTimeField(auto_now=True)
  ## to change in admin
  class Meta:
    verbose_name ='category'
    verbose_name_plural ='categories'
  def clean(self)  :
    self.category_name=self.category_name.capitalize()
    
  def __str__(self):
    return self.category_name





#FoodItem
class Product_Menu(models.Model):
  vendor        = models.ForeignKey(Vendor,on_delete=models.CASCADE)
  category      = models.ForeignKey(Category,on_delete=models.CASCADE,related_name ='product_items')
  #food title = product_title

  product_title = models.CharField(max_length=50)
  slug          = models.SlugField(max_length=50, unique=True)
  description   = models.TextField(max_length=250, unique=True)
  price         = models.DecimalField(max_digits=10, decimal_places=2)

  product_itemno = models.CharField(max_length=20, unique=True)
  cost_price    = models.DecimalField(max_digits=10, decimal_places=2)
  
  image = models.ImageField(upload_to ='product_images' ) 
  is_available = models.BooleanField(default=True)

  created_at    = models.DateTimeField(auto_now_add=True)
  updated_at    = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.product_title

    
