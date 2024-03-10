from django.shortcuts import redirect, render, HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

from .error_printscr import print_message


# Create your views here.


def registerUser(request):
  if request.method=='POST':
    mess = f'  **joven**  request.POST ------->:{request.POST}'
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

