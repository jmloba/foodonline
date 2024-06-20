from django.contrib import admin
from .models import Payment, Order,OrderedFood




class OrderedFoodInline(admin.TabularInline):
  model=OrderedFood
  readonly_fields = ['order','payment','user','product_item','quantity','price','amount','created_at','updated_at']
  extra=0
class OrderAdmin(admin.ModelAdmin):
  list_display=['user','payment','order_number','first_name','total','tax_data','payment_method','is_ordered','status'] 

  inlines=[OrderedFoodInline]
                 
  ordering=('-order_number',)
  # list_editable =('payment_method','is_ordered')
  filter_horizontal =()
  list_filter =()
  fieldsets=()   

class PaymentAdmin(admin.ModelAdmin):
  list_display=['user','transaction_id','paypal_transaction_id','payment_method','status','created_at','amount'] 
                  
  ordering=('-created_at',)
  list_editable =('amount','payment_method')
  filter_horizontal =()
  list_filter =()
  fieldsets=() 
 

admin.site.register(Payment,PaymentAdmin)  
admin.site.register(OrderedFood)  
admin.site.register(Order,OrderAdmin)  

