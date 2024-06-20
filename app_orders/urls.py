from django.urls import path, include
from . import views
from accounts import views as AccountViews

app_name='app_orders'

urlpatterns = [
path('place-order/', views.place_order, name ='place-order'),
path('save-to-payment/', views.save_to_payment, name ='save-to-payment'),
path('order_complete/', views.order_complete, name ='order-complete'),

]