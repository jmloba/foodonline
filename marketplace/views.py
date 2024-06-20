from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .context_processor import get_cart_counter,get_cart_amount
from django.db.models import Q

from vendor.models import Vendor,OpeningHour
from menu.models import Category,Product_Menu
from marketplace.models import Cart
from accounts.models import UserProfile

from app_orders.forms  import OrderForm

from vendor.views import get_vendor

from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # 'D' is a shortcut for Distance
from django.contrib.gis.db.models.functions import Distance
from datetime import time, datetime, date


@login_required(login_url='login')   
def checkout(request):

  cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
  cart_count=cart_items.count()
  if cart_count <=0 :
    return redirect('marketplace:marketplace')
  
  user_profile = UserProfile.objects.get(user=request.user)
  default_values = {
    'first_name': request.user.first_name,
    'last_name': request.user.last_name,
    'email': request.user.email,
    'phone': request.user.phone_number,

    'address': user_profile.address,
    'city':user_profile.city,
    'state': user_profile.state,
    'pin_code' :user_profile.zip_code,
    'country':user_profile.country
  }

  print(f' default values are : **** {default_values}')
  print(f'user from request : {request.user}')

  form = OrderForm(initial=default_values)
  
  context={'form':form, 'cart_items':cart_items,"cart_count":cart_count}
  return render(request,'marketplace/checkout.html', context)

# Create your views here.

def marketplace(request):
  vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
  vendor_count = vendors.count()
  context = {'vendors':vendors,'vendor_count':vendor_count,}
  return render(request,'marketplace/listings.html',context)

def vendor_detail(request, vendor_slug):
  vendor = get_object_or_404(Vendor, vendor_slug = vendor_slug)
  categories = Category.objects.filter(vendor = vendor).prefetch_related(
    Prefetch(
      'product_items' , queryset=Product_Menu.objects.filter(is_available=True))
  )

  opening_hours =  OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour') 

  today_date=date.today()
  today =today_date.isoweekday()
  
  current_opening_hours = OpeningHour.objects.filter(vendor=vendor,day=today)
  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
  else:
    cart_items  = None

   


  context={
    "vendor":vendor,
    'categories':categories, 
    'cart_items': cart_items,
    'opening_hours':opening_hours,
    'current_opening_hours' : current_opening_hours,
        
    }
  return render(request,'marketplace/vendor_detail.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def add_to_cart(request, product_id):
  if request.user.is_authenticated:
    if  is_ajax(request=request):
      try :
        product_item = Product_Menu.objects.get( id = product_id)
        # check if the user added the product to the cart
        try:
          checkCart= Cart.objects.get(user=request.user, product_item = product_item)
          # increase cart quantity
          checkCart.quantity += 1
          checkCart.save()
          return JsonResponse({'status':'success','message':'Increased quantity to the cart',
                               'cart_counter': get_cart_counter(request),
                               'qty':checkCart.quantity,
                               'cart_amount' :get_cart_amount(request),

                               })
        except:
          checkCart= Cart.objects.create(user=request.user, product_item = product_item, quantity = 1)

          return JsonResponse({'status':'success','message':'created  and added quantity to the cart', 
                               'cart_counter': get_cart_counter(request),
                               'qty':checkCart.quantity,
                               'cart_amount' :get_cart_amount(request),

                               })
      except:
        return JsonResponse({'status':'Failed','message':'xxxx This product does not exists'})
    else:
      return JsonResponse({'status':'Failed','message':'Please login to continue'})
  else:
    return JsonResponse({'status':'login_required','message':'Please login to continue'})
  # return HttpResponse(f'product id : {product_id}')

def decrease_cart(request, product_id):
  if request.user.is_authenticated:
    if  is_ajax(request=request):
      try :
        product_item = Product_Menu.objects.get( id = product_id)
        # check if the user added the product to the cart
        try:
          checkCart= Cart.objects.get(user=request.user, product_item = product_item)
          if checkCart.quantity > 1 :
          # increase cart quantity
            checkCart.quantity -= 1
            checkCart.save()
          else :
            checkCart.delete()
            checkCart.quantity = 0
          return JsonResponse({'status':'Success','message':'cart quantity is already 0',
                                'cart_counter': get_cart_counter(request),
                                'qty':checkCart.quantity,
                                'cart_amount' :get_cart_amount(request),

                                })
        except:
          return JsonResponse({'status':'Failed','message':'no record found...', 
                               })
      except:
        return JsonResponse({'status':'Failed','message':'xxxx This product does not exists'})
    else:
      return JsonResponse({'status':'Failed','message':'Please login to continue'})
  else:
    return JsonResponse({'status':'login_required','message':'Please login to continue'})  

@login_required(login_url='login')  
def cart(request):
  cart_items= Cart.objects.filter(user=request.user).order_by('created_at') 
  
  context ={"cart_items":cart_items}
  return render(request,'marketplace/cart.html',context)

def delete_cart(request,cart_id):
    if request.user.is_authenticated:
      if  is_ajax(request=request):
        try:
          # check if cart item exist
          cart_item = Cart.objects.get(user = request.user, id=cart_id)
          if cart_item:
            print(f'deleting item in cart_item : {cart_item.product_item}, --->> quantity : {cart_item.quantity}')
            
            cart_item.delete()
            return  JsonResponse({'status':'Success',
                                  'message':'cart item has been deleted',
                                  'cart_counter': get_cart_counter(request),
                                  'cart_amount' :get_cart_amount(request),

                                    })
        except:
           return  JsonResponse({'status':'Failed','message':'cart item does not exist', })
      else:
        return JsonResponse({'status':'Failed','message':'no record found...', })

def search(request):
  if not 'address' in request.GET:
    return redirect('marketplace')
  else:
    address = request.GET['address']
    latitude =request.GET['lat']
    longitude =request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
 
    print( f' address : {address}\n latitude : {latitude}\n longitude : {longitude}\n radius : {radius}\n search product or name : {keyword}')
    # geet bendor id that has food item the user is looking for 
    fetch_vendor_by_product_item = Product_Menu.objects.filter(
      product_title__icontains=keyword, is_available = True).values_list('vendor',flat=True)
    
    # vendors = Vendor.objects.filter(Q(id__in=fetch_vendor_by_product_item) | 
    #                                 Q(vendor_name__icontains=keyword,  is_approved=True,  user__is_active=True,))

    if latitude and longitude and radius:
      pnt = GEOSGeometry('POINT(%s %s)' %(longitude, latitude))
      vendors =Vendor.objects.filter(
        Q(id__in=fetch_vendor_by_product_item) | 
        Q(vendor_name__icontains=keyword,  is_approved=True,  user__is_active=True),
        user_profile__location__distance_lte = (pnt,D(km=radius))
        ).annotate(distance123=Distance("user_profile__location",pnt)).order_by("distance123") 
      for v in vendors:
        v.kms = round(v.distance123.km,1)

    print(f'product menu : {fetch_vendor_by_product_item} ')
    # search for restaurant
  
    vendor_count = vendors.count
    print(f'search for vendors : {vendors}')
    context={'vendors':vendors, 'vendor_count':vendor_count,  'source_location':address         }
    return render(request,'marketplace/listings.html', context)
 