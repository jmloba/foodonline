from django.contrib import admin

from vendor.models import Vendor,OpeningHour


class VendorAdmin(admin.ModelAdmin):

  list_display=('id','user','vendor_name','user_profile','created_at','is_approved')

  list_display_links = ('user','vendor_name')
  list_editable =('is_approved',)


class OpeningHourAdmin(admin.ModelAdmin):
  list_display=('vendor','day','from_hour','to_hour','is_closed',
                'created_at','modified_at' )

  list_editable =('day','is_closed','from_hour','to_hour',)
  filter_horizontal =()
  list_filter =()
  fieldsets=() 

admin.site.register(Vendor,VendorAdmin)
admin.site.register(OpeningHour,OpeningHourAdmin)