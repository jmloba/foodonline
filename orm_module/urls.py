from django.urls import path
from . import views


urlpatterns = [
  path('orm_module/', views.orm_sample_1, name = "orm_sample_1"),
  path('orm_query/', views.orm_query_union, name = "orm_query_union"),
  path('orm_query_not/', views.orm_query_union_not, name = "orm_query_union_not"),
  path('orm_query_direct/', views.orm_query_direct, name = "orm_query_direct"),
  path('orm_model_inheritance/', views.orm_model_inheritance, name = "orm_model_inheritance"),  

  path('orm_product_all/', views.product_all, name = "product_all"),

]
