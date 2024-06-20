
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator  

from accounts.utils import detectUser, send_verification_email
from django.core.exceptions import PermissionDenied

from django.utils.http import  urlsafe_base64_decode 

from vendor.forms import VendorRegistrationForm
from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from accounts.models import UserProfile
from django.template.defaultfilters import slugify

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
      return redirect('myAccount')
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
      vendor_name =v_form.cleaned_data
      vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)

      
      user_profile =UserProfile.objects.get(user=user)
      vendor.user_profile =user_profile
      vendor.save()

      ''' SEND Verification Email'''
      mail_subject= 'Please Activate your Account ' 
      email_template = 'accounts/email/account_verification.html'      
      send_verification_email(request,user,mail_subject,email_template )
      ''' SEND Verification Email *** END'''


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
      return redirect('myAccount')
  elif request.method=='POST':  
   
    form = UserForm(request.POST)
    if form.is_valid():
       
       #-->> 1st way to save and hash password --> using form
      # password = form.cleaned_data['password']
      # user = form.save(commit=False)
      # user.set_password(password)
      # user.role = User.CUSTOMER
      # user.save()
      
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

      ''' SEND Verification Email'''
      mail_subject= 'Please Activate your Account ' 
      email_template = 'accounts/email/account_verification.html'      
      send_verification_email(request,user,mail_subject,email_template )
      ''' SEND Verification Email *** END'''
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
  print(f'\n\ncustomer dashboard   ***: {request.user}\n')

  context={}
  return render(request,'accounts/dashboardCustomer.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def dashboardVendor(request):
    
  vendor = Vendor.objects.get(user=request.user)
  context={'vendor':vendor,}
  return render(request,'accounts/dashboardVendor.html',context)

@login_required(login_url='login')
def dashboardAdmin(request):
  return render(request,'accounts/dashboardAdmin.html')


''' for email activation '''

def activate(request, uidb64, token):
   # Activate the user by setting the is_active status to true
  try: 
    uid =  urlsafe_base64_decode(uidb64).decode()
    user =User._default_manager.get(pk=uid)
    
  except(TypeError,ValueError,OverflowError,User.DoesNotExist):
    user=None


  if user is not None and default_token_generator.check_token(user,token):
    user.is_active = True
    user.save()
    messages.success(request,'Congratulations, Your account is now active')
    return redirect('myAccount')
  else:
    messages.error(request,'Invalid activation link')
    return redirect('myAccount')






''' password section'''
def forgot_Password(request):
  if request.method =='POST':
    email=request.POST['email']
    if User.objects.filter(email=email).exists():
      user=User.objects.get(email__exact=email)
      # send reset password email

      mail_subject= 'Reset Password' 
      email_template = 'accounts/email/reset_Password_email.html'

      send_verification_email(request,user,mail_subject,email_template)

      
      messages.success(request,'We have sent you the link thru your email')
      return redirect('login')
    else:
      messages.success(request,'Account does not exist')
      return redirect('forgot_Password')            
  return render(request,('accounts/forgot_Password.html'))

def reset_Password_validate(request, uidb64, token):
  try: 
    ''' note uid is a primary key from the link'''
    uid =  urlsafe_base64_decode(uidb64).decode()
    user =User._default_manager.get(pk=uid)
  except(TypeError,ValueError,OverflowError,User.DoesNotExist):
    user=None  

  if user is not None and default_token_generator.check_token(user,token):
    request.session['uid']= uid
    messages.info(request,'Please reset you password')


    return redirect('reset_Password')
  else:
    messages.error(request,'This link has been expired')
    return redirect('myAccount')


  return render(request,('accounts/reset_Password_validate.html'))

def reset_Password(request):
  if request.method =='POST':
    password1=request.POST['password1']
    password2=request.POST['password2']
    messages.info(request,f'password1:{password1}  password2 :{password2} ')
    if password1==password2:
      pk = request.session.get('uid')
      user =User.objects.get(pk=pk)
      user.set_password(password1)
      user.is_active = True
      user.save()
      messages.success(request,'Password reset successfull')
      return redirect('login')
    else:
      messages.success(request,'Password does not match')
      return redirect('reset_Password')

    #   user.is_active = True
    #   user.save()
    #   messages.success(request,'Congratulations, Your account is now active')
    #   return redirect('myAccount')
  return render(request,('accounts/reset_Password.html'))





