from django.contrib import admin
from .models import InvoiceMaster

# Register your models here.

class InvoiceMasterAdmin(admin.ModelAdmin):
  list_display=('id','invoice_no','invoice_desc')

  list_editable =('invoice_desc',)
  filter_horizontal =()
  list_filter =()
  fieldsets=() 
 
admin.site.register(InvoiceMaster,InvoiceMasterAdmin)