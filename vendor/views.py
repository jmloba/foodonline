from django.shortcuts import get_object_or_404, redirect, render
from vendor.forms import VendorRegistrationForm

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,Product_Menu
from menu.forms import CategoryForm,ProductItemForm
from django.template.defaultfilters import slugify

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
       category.slug= slugify(category_name)
       form.save()
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
    form.fields['category'].queryset = Category.objects(vendor=get_vendor(request))


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


