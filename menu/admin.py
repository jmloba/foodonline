from django.contrib import admin
from .models import Category, Product_Menu


class CategoryAdmin(admin.ModelAdmin):
  list_display=['category_name','slug','description']  
  ordering=('category_name',)
  prepopulated_fields={'slug':('category_name',)}

  # note : if search field is a foreign key use "double underscore" i.e : vendor__vendor_name
  search_fields=('category_name','vendor__vendor_name')

  filter_horizontal =()
  list_filter =()
  fieldsets=() 

class Product_MenuAdmin(admin.ModelAdmin)  :             
  prepopulated_fields={'slug':('product_title',)}  
  list_display=['id','vendor','category','product_itemno','product_title','slug','description','price','is_available']
  list_editable =('is_available',)
  ordering=('product_title',)
  search_fields=('product_title','description','category__category_name')
  filter_horizontal =()
  list_filter =()
  fieldsets=()
                 
                    
                    

# Register your models here.
# to change the view in admin ie. put category admin 
# change view  
  
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product_Menu,Product_MenuAdmin)