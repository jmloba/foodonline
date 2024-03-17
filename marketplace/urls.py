from django.urls import path
from . import views


urlpatterns = [
  path('', views.marketplace, name = "marketplace"),
  path('<slug:vendor_slug>/',views.vendor_detail,name='vendor_detail' ),

  # add to cart
  path('add_to_cart/<int:product_id>', views.add_to_cart, name ='add_to_cart'),
  path('decrease_cart/<int:product_id>', views.decrease_cart, name ='decrease_cart')

]
