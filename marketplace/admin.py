from django.contrib import admin

from .models import Cart

class CartAdmin(admin.ModelAdmin):
  list_display=['id','user', 'product_item','quantity']
  filter_horizontal =()
  list_filter =()
  fieldsets=()
  ordering=('user',)





# Register your models here.
admin.site.register(Cart, CartAdmin)
