from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render
from .context_processor import get_cart_counter,get_cart_amount
from vendor.models import Vendor
from menu.models import Category,Product_Menu
from vendor.views import get_vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test
from marketplace.models import Cart


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
  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
  else:
    cart_items  = None


  context={
    "vendor":vendor,
    'categories':categories, 
    'cart_items': cart_items}
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

