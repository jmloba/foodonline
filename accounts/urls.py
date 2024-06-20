from django.urls import path, include
from . import views

urlpatterns = [
  path('',views.myAccount),
  path('registerUser/', views.registerUser, name ='registerUser' ),
  path('registerVendor/', views.registerVendor, name ='registerVendor' ),  

  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout')  ,

  path('myAccount/', views.myAccount, name='myAccount')  , 

  path('dashboardCustomer/', views.dashboardCustomer, name='dashboardCustomer')  ,  

  
  path('dashboardVendor/'  , views.dashboardVendor  , name='dashboardVendor')  ,  
 
  path('dashboardAdmin/'   , views.dashboardAdmin   , name='dashboardAdmin')  ,  
  # called from email
  path('activate/<uidb64>/<token>/', views.activate, name ='activate'),

  path('forgot_Password/', views.forgot_Password, name ='forgot_Password'),  
  path('reset_Password_validate/<uidb64>/<token>/', views.reset_Password_validate, name ='reset_Password_validate'),    
  path('reset_Password/', views.reset_Password, name ='reset_Password'),  

  path('vendor/', include('vendor.urls'))


]
