from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_customer
from accounts.models import User, UserProfile
from accounts.forms import UserProfileForm, UserInfoForm
from django.contrib import messages
from app_orders.models import Order, OrderedFood
import simplejson as json

# Create your views here.
def test_customer(request):
  print('test customer')
  context={}
  return render(request,'app_customers/customer-test.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)

def cprofile(request):
  profile = get_object_or_404(UserProfile, user = request.user)
  if request.method=='POST':
    profile_form = UserProfileForm(request.POST, request.FILES, instance = profile)

    user_form = UserProfileForm(request.POST, instance = request.user)
    if profile_form.is_valid() and user_form.is_valid():
      profile_form.save()
      user_form.save()
      messages.success('profile saved')
      return redirect ('app_customers:cprofile')
    else:
      print(profile_form.errors)
      print(user_form.errors)



  else :
    profile_form = UserProfileForm(instance = profile)
    user_form = UserInfoForm(instance = request.user)
  
  

  context={'profile_form':profile_form, 'user_form':user_form, 'profile': profile} 
  return render(request,'app_customers/cprofile.html', context)

def my_orders(request):
  orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
  context={'orders':orders}
  return render(request,'app_customers/my-orders.html', context)

def order_details(request,order_number=None):
  try :
    order = Order.objects.get(order_number=order_number, is_ordered=True)

    ordered_food = OrderedFood.objects.filter(order=order)

    subtotal= 0

    for item in ordered_food:
      subtotal += (item.quantity * item.price)

    tax_data = json.loads(order.tax_data)


  except:  
    return redirect('app_customers:customer')

  
  context={'order':order, 
           'ordered_food':ordered_food,
           'subtotal':subtotal,
           'tax_dict': tax_data
           }
  return render(request,'app_customers/order-details.html', context)

