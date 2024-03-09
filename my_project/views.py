from django.shortcuts import render, HttpResponse
# from employees.models import Employee


def home(request):

  # # get the list of employees that is stored in the database
  # employees = Employee.objects.all()

  name = 'joven'
  context={'name':name}

  # print(f'employees are {employees}')

  # return render(request,'home.html', context)
  return HttpResponse('hello world')
