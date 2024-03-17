from django.shortcuts import render, HttpResponse
# from employees.models import Employee
from vendor.models import Vendor


def home(request):
  name = 'joven'

  vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
  context={'name':name, 'vendors':vendors}

  return render(request,'main_project/home.html', context)
