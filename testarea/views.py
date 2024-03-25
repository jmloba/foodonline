
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse,JsonResponse
from .models import InvoiceMaster
from orm_module.models import Student
from .forms import InvoiceMasterForm , Student_form
from django.db.models import Q
from django.contrib import messages
from accounts.utils import is_ajax
# Create your views here.

def test_main(request):
  students = Student.objects.all()
 

  if (request.method=='POST'):
    # pickup data from input form 
    form = Student_form(request.POST)
 
    if form.is_valid():
      firstname = form.cleaned_data['firstname']
      lastname = form.cleaned_data['lastname']
      email = form.cleaned_data['email']
      age = form.cleaned_data['age']
      classroom = form.cleaned_data['classroom']

      print(f'firstname: {firstname}, lastname : {lastname}, email:{email}, age: {age}, classroom : {classroom}   ')
      
      form.save()
    else:
      print(f'invalid form :{form.errors}')
      context={'students':students, 'form':form}
      return render(request,'testarea/test1.html',context)


  form = Student_form() 
  context={'students':students, 'form': form}

  return render(request,'testarea/test1.html',context)

def testremove_record(request,pk:None):
  print('inside :student list')
  if request.user.is_authenticated:
    print('request is authenticated')
    if is_ajax(request) :
      print(f'value of id passed : {pk}')
      student_record =get_object_or_404(Student,pk=pk)

      student_record.delete()

      response ={'status':'success','message':'record has been deleted','id':pk}
      return JsonResponse(response)
    else:
      print('not ajax request ')  
  else:
    print('not authenticated')    

  return HttpResponse('remove from list student')






    