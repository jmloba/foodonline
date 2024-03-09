from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User

class CustomerUserAdmin(UserAdmin):
  list_display=(
    'email',
    'first_name',
    'last_name', 
    'phone_number', 
    'username','is_active','is_superadmin','role','date_joined'
    
                )
  ordering=('email',)

  filter_horizontal =()
  list_filter =()
  fieldsets=()


# Register your models here.

admin.site.register(User,CustomerUserAdmin)
