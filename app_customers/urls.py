from django.urls import path, include
from . import views
from accounts import views as AccountViews

app_name='app_customers'

urlpatterns = [
  path('customer-test/', views.test_customer, name='customer-test' ),

  path('', AccountViews.dashboardCustomer, name='customer' ),  
  path('cprofile/', views.cprofile, name='cprofile' ),  

]