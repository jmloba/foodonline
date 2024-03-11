from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from vendor.forms import VendorRegistrationForm
from .forms import UserForm
from .models import User, UserProfile
from accounts.models import UserProfile
from accounts.utils import detectUser
from django.core.exceptions import PermissionDenied

from .error_printscr import print_message

'''
restrict the vendor from accessing customer page
restrict the customer from accessing vendor page
'''
def check_role_vendor(user):
  if user.role == 1: # role is vendor
    return True
  else:
    raise PermissionDenied

def check_role_customer(user):
  if user.role == 2: # role is customer
    return True
  else:
    raise PermissionDenied



def registerVendor(request):
  if request.user.is_authenticated:
      messages.warning(request,'You are already logged in ')
      return redirect('dashboard')
  elif request.method=='POST':  

    mess = f'  **joven** register vendor  request.POST ------->:{request.POST}'
    print_message(mess)
    
    form = UserForm(request.POST)
    v_form = VendorRegistrationForm(request.POST,request.FILES)
    if form.is_valid()  and v_form.is_valid() :

      mess = f' **joven** form is valid: form:{form.is_valid()}, v_form : { v_form.is_valid()} '
      print_message(mess)

      ''' create vendor using create_user method'''
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']

      user = User.objects.create_user(
        first_name=first_name, 
        last_name=last_name,
        username=username,
        email=email,
        password=password
        )
      
      user.role = User.VENDOR
      user.save()
      vendor =v_form.save(commit=False)
      vendor.user = user
      
      user_profile =UserProfile.objects.get(user=user)
      vendor.user_profile =user_profile
      vendor.save()

      messages.success(request,'Your account (Vendor)has been registered successfully, Please wait for the approval')
      return redirect('registerVendor')
    else:  
      mess = f' **joven** form is  invalid : register form ### '
      print_message(mess)    
  else:  
    form   = UserForm()
    v_form = VendorRegistrationForm()
  context ={'form':form, 'v_form':v_form  }
  return render(request,'accounts/registerVendor.html',context )  


def registerUser(request):
  if request.user.is_authenticated:
      messages.warning(request,'You are already logged in ')
      return redirect('dashboard')
  elif request.method=='POST':  


    mess = f'  **joven** registeer user request.POST ------->:{request.POST}'
    print_message(mess)
    
    form = UserForm(request.POST)
    if form.is_valid():

      mess = f' **joven** form is valid: calling forms.save'
      print_message(mess)

      ''' #-->> 1st way to save and hash password --> using form
      password = form.cleaned_data['password']
      user = form.save(commit=False)
      user.set_password(password)
      user.role = User.CUSTOMER
      user.save()
      '''

      ''' create user using create_user method'''
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = User.objects.create_user(
        first_name=first_name, 
        last_name=last_name,
        username=username,
        email=email,
        password=password
        )
      user.role = User.CUSTOMER
      user.save()

      messages.success(request,'Your account has been registered successfully')

      mess = f'**joven**   views.accounts--->> user is created : {username}'
      print_message(mess)      


      return redirect('registerUser')
    else : #---> form is not valid 
      mess = f'**joven** views.accounts : invalid form -->>> form errors : {form.errors}'
      print_message(mess)   
      # return redirect('registerUser')
  else:
    form = UserForm()

  context = {'form': form,  }
  return render(request,'accounts/registerUser.html',context )

def login(request):
  if request.user.is_authenticated:
      messages.warning(request,'You are already logged in ')
      return redirect('myAccount')
  elif request.method=='POST':
    email =request.POST['email']
    password =request.POST['password']
    user = auth.authenticate(email=email, password=password)
    if user is not None:
      auth.login(request,user)
      messages.success(request,'logged in successfully')         
      return redirect('myAccount')

    else:  
      messages.warning(request,'Invalid login credentials ')
      return redirect('login')
 
  return render(request,'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.success(request,'logged out successfully')

  return redirect('login')

# def dashboard(request):
#   return render(request,'accounts/dashboard.html')


''' this function is beinng called from utils.py
def detectUser(user):
  if user.role == 1:
    redirectUrl ='dashboardVendor'
  elif  user.role == 2:
    redirectUrl ='dashboardCustomer'
  elif  user.role == None and user.is_superadmin:
    redirectUrl ='/admin'

  return redirectUrl

'''
@login_required(login_url='login')
def myAccount(request):
  # these function will call utils.py
  user = request.user
  redirectUrl= detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def dashboardCustomer(request):
  return render(request,'accounts/dashboardCustomer.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def dashboardVendor(request):
  return render(request,'accounts/dashboardVendor.html')

@login_required(login_url='login')
def dashboardAdmin(request):
  return render(request,'accounts/dashboardAdmin.html')





