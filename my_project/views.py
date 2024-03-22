from django.shortcuts import render, HttpResponse

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # 'D' is a shortcut for Distance
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q

# from employees.models import Employee
from vendor.models import Vendor

def get_or_set_current_location(request):
  if 'lat' in request.session:
    lat = request.session['lat']
    lng = request.session['lng']
    return lng, lat
  elif 'lat' in request.GET: 
    # ie if the user click the location then lat and lon is in url parameter
    #get lat and lng from url parameter
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    # save lat and lng to the session
    request.session['lat'] = lat
    request.session['lng'] = lng
    return lng, lat
  else:
    return None


def home(request):
  if get_or_set_current_location(request) is not None:
    # lat=request.GET.get('lat') 
    # lng=request.GET.get('lng') 

    # pnt = GEOSGeometry('POINT(%s %s)' %(lng, lat))
    pnt = GEOSGeometry('POINT(%s %s)' %(  get_or_set_current_location(request) ))
    vendors =Vendor.objects.filter(

        user_profile__location__distance_lte = (pnt,D(km=50))
        ).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance") 
    for v in vendors:
      v.kms = round(v.distance.km,1)
  else :    
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]


  name = 'joven'
  context={'name':name, 'vendors':vendors}

  return render(request,'main_project/home.html', context)
