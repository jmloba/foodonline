from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from vendor.forms import VendorRegistrationForm, OpeningHourForm

from accounts.forms import UserProfileForm 
from accounts.models import UserProfile
from .models import Vendor,OpeningHour
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,Product_Menu
from menu.forms import CategoryForm,ProductItemForm
from django.template.defaultfilters import slugify
from accounts.utils import is_ajax

# Create your views here.
def get_vendor(request):
  vendor = Vendor.objects.get(user=request.user) 
  return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):

  profile = get_object_or_404(UserProfile, user=request.user)
  vendor = get_object_or_404(Vendor, user=request.user)

  if request.method=='POST':
    profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    vendor_form =VendorRegistrationForm(request.POST, request.FILES, instance=vendor)
    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      messages.success(request,'Settings updated')
      return redirect('vprofile')
    else:
      print(profile_form.errors)
      print(vendor_form.errors)
  else:     

  # note : to pass the value inside the form *** you need instance
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorRegistrationForm(instance=vendor)

  context = { 'vendor_form' : vendor_form , 'profile_form' : profile_form , 'profile': profile, 'vendor':vendor}

  return render(request,'vendor/vprofile.html', context )

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
  # get loggedin user
  vendor = get_vendor(request)
  categories = Category.objects.filter(vendor=vendor).order_by('created_at')
  context ={"categories":categories,'vendor':vendor}
  return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
  vendor = get_vendor(request)
  category =get_object_or_404(Category,pk=pk)
  productItems = Product_Menu.objects.filter(vendor=vendor,category=category)

  context={'productItems' : productItems, 'category':category}
  return render(request,'vendor/fooditems_by_category.html',context)

'''
crud operations for category
'''
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_category_add(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
       category_name = form.cleaned_data['category_name']
       category = form.save(commit=False)
       category.vendor =get_vendor(request)

       category.save()

       category.slug= slugify(category_name) +'-'+str(category.id)
       category.save()
       messages.success(request, 'Category was added successfuly')
       return redirect('menu_builder')
    else :
      messages.info(request, form.errors)
      print(form.errors)
  else:
    form = CategoryForm()
  context={'form':form,}
  return render(request,'vendor/product_category_add.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_category_edit(request,pk=None):
  category = get_object_or_404(Category,pk=pk)
  if request.method == 'POST':
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
       category_name = form.cleaned_data['category_name']
       category = form.save(commit=False)
       category.vendor =get_vendor(request)
       category.slug= slugify(category_name)
       form.save()
       messages.success(request, 'Category was update successfuly')
       return redirect('menu_builder')
    else :
      messages.info(request, form.errors)
      print(form.errors)
  else:
    form = CategoryForm(instance=category)
  context={'form':form,'category':category}
  return render(request,'vendor/product_category_edit.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_category_delete(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request, 'Category was deleted successfuly')
    return redirect('menu_builder')

''' 
--------------------------------------------------------
crud operations for product items
--------------------------------------------------------
'''
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_item_add(request):
  if request.method == 'POST':
    form = ProductItemForm(request.POST, request.FILES)

    if form.is_valid():
        product_title = form.cleaned_data['product_title']

        product = form.save(commit=False)
        product.vendor =get_vendor(request)
        product.slug= slugify(product_title)
        form.save()

        messages.success(request, 'Product item was added successfuly')
        return redirect('fooditems_by_category',product.category.id)
    else :
      messages.info(request, form.errors)
      print(form.errors)
  else:
    form = ProductItemForm()
    # filter category
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))


  context={'form':form,}
  return render(request,'vendor/product_item_add.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_item_edit(request,pk=None):
  product = get_object_or_404(Product_Menu,pk=pk)

  if request.method == 'POST':
    form = ProductItemForm(request.POST, request.FILES,instance=product)
    if form.is_valid():
      product_title = form.cleaned_data['product_title']

      product = form.save(commit=False)
      product.vendor =get_vendor(request)
      product.slug= slugify(product_title)
      form.save()
      messages.success(request, 'Category was updated successfuly')
      return redirect('fooditems_by_category',product.category.id)
    else :
      messages.info(request, form.errors)
      print(form.errors)
  else:
    form = ProductItemForm(instance=product)
    form.fields['category'].queryset = Category.objects(vendor=get_vendor(request))
  
  context={'form':form,'product':product}
  return render(request,'vendor/product_item_edit.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_item_delete(request,pk=None):
  product = get_object_or_404(Product_Menu,pk=pk)
  product.delete()
  messages.success(request, 'Product was deleted successfuly')
  return redirect('fooditems_by_category',product.category.id)

# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def opening_hours(request):
  opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
  form = OpeningHourForm()
  context = {'form': form, 
             'opening_hours':opening_hours}
  return render(request,'vendor/openinghours.html', context)

def add_opening_hours(request):

  if request.user.is_authenticated:
    if is_ajax(request) and request.method == 'POST':
      if request.headers.get('x-requested-with')  =='XMLHttpRequest' and request.method=='POST':

        day = request.POST.get('day')
        from_hour= request.POST.get('from_hour')
        to_hour= request.POST.get('to_hour')
        is_closed= request.POST.get('is_closed')
        print(f"------->>>>  inside views -->>variables are day : {day}, from hour : {from_hour}, to hour : {to_hour}, is_closed : {is_closed} <<<<<-----\n")
        try:
          hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour = from_hour, to_hour=to_hour,is_closed=is_closed)
          if hour:
            day=OpeningHour.objects.get(id=hour.id)
            if day.is_closed:
              response ={'status':'success','id':hour.id,'day':day.get_day_display(), 'is_closed':'closed'}
            else:  
              response ={'status':'success','id':hour.id,'day':day.get_day_display(),'from_hour':day.from_hour,'to_hour':day.to_hour}

          return JsonResponse(response)
        except IntegrityError as e:
          response ={'status':'failed','message': from_hour+ ' - ' + to_hour +' already exist','error':str(e) }
          return JsonResponse(response)
      else: 
        return HttpResponse('invalid request')
    else: # ajax else
     
      HttpResponse('failed to add, invalid request')

def remove_opening_hours(request,pk=None):
  print('inside : remove_opening_hours')
  if request.user.is_authenticated:
    print('request is authenticated')
    if is_ajax(request) :
      print(f'value of id passed : {pk}')
      hour =get_object_or_404(OpeningHour,pk=pk)

      hour.delete()

      response ={'status':'success','message':'record has been deleted','id':pk}
      return JsonResponse(response)
    else:
      print('not ajax request ')  
  else:
    print('not authenticated')    

  return HttpResponse('remove opening hours ')


  
