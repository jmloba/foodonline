from django.contrib import admin

from .models import Cart, Tax

class CartAdmin(admin.ModelAdmin):
  list_display=['id','user', 'product_item','quantity']
  filter_horizontal =()
  list_filter =()
  fieldsets=()
  ordering=('user',)

class TaxAdmin(admin.ModelAdmin):
  list_display=['id','tax_type', 'tax_percentage','is_active']
  list_editable =('tax_type','tax_percentage','is_active')
  filter_horizontal =()
  list_filter =()
  fieldsets=()



# Register your models here.
admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
 