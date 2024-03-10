from django.contrib import admin

from vendor.models import Vendor


class VendorAdmin(admin.ModelAdmin):

  list_display=('user','vendor_name','user_profile','created_at','is_approved')

  list_display_links = ('user','vendor_name')



# Register your models here.
admin.site.register(Vendor,VendorAdmin)
