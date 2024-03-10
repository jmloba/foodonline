from django.shortcuts import redirect, render, HttpResponse

from vendor.forms import VendorRegistrationForm
from .forms import UserForm
from .models import User, UserProfile
from accounts.models import UserProfile
from django.contrib import messages

from .error_printscr import print_message


# Create your views here.
def registerVendor(request):
  if request.method=='POST':
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
  if request.method=='POST':
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

