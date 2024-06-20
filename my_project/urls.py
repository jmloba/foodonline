"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

from marketplace import views as martketplaceViews
import debug_toolbar

urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),

    path('', include('accounts.urls')),
    path('marketplace/',include('marketplace.urls')),
    path('vendor/',include('vendor.urls')),
    path('app_customers/',include('app_customers.urls')),
    path('app_orders/',include('app_orders.urls')),
    # cart page
    path('cart/', martketplaceViews.cart, name ='cart'),
    #search
    path('search/', martketplaceViews.search, name ='search'),
    #CHECKOUT
    path('checkout/', martketplaceViews.checkout, name ='checkout'),

    path('orm_module/', include('orm_module.urls')),
    path('__debug__/',include(debug_toolbar.urls)),
    path('testarea/', include('testarea.urls')),    



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

