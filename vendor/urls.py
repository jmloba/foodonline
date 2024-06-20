from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
  path('',AccountViews.dashboardVendor, name='vendor' ),
  path('profile/', views.vprofile, name = "vprofile"),
  path('menu-builder/', views.menu_builder, name ='menu_builder'),
  path('menu-foodlist/category/<int:pk>', views.fooditems_by_category, name ='fooditems_by_category'),
  
  # vendor - category CRUD
  path('menu-builder/category/add', views.product_category_add, name ='product_category_add'),
  path('menu-builder/category/edit/<int:pk>', views.product_category_edit, name ='product_category_edit'),
  path('menu-builder/category/delete/<int:pk>', views.product_category_delete, name ='product_category_delete'),

  # food item CRUD
  path('menu-builder/product-item/add', views.product_item_add, name ='product_item_add'),
  path('menu-builder/product-item_edit/<int:pk>', views.product_item_edit, name ='product_item_edit'),
  
  path('menu-builder/product-item_delete/<int:pk>', views.product_item_delete, name ='product_item_delete'),

  # opening hours CRUD
  path('opening_hours/', views.opening_hours, name ='opening_hours'),

  path('opening_hours/add/', views.add_opening_hours, name ='add_opening_hours'),

  
  path('opening_hours/remove/<int:pk>/', views.remove_opening_hours, name ='remove_opening_hours'),
]

