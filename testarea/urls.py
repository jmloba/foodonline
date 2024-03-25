from django.urls import path, include
from . import views


urlpatterns = [
  path('test/',views.test_main, name='test_main' ),
  path('test/remove/<int:pk>/',views.testremove_record, name='testremove_record' ),
  
  
]
