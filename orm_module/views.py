
from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Teacher,Product, poly1Project, poly1ArtProject, poly1ResearchProject
from django.db import connection
from django.db.models import Q

# for direct connection 

# Create your views here.

'''  ==========================================================
part 2 select  all
 ========================================================== '''

def orm_sample_1_(request):
  routine_name  = 'orm_sample_1'
  students = Student.objects.all()
  myquery = students.query
  context={'routine_name':routine_name,
           'students': students,
           'myquery': myquery
           }
  return render(request,'orm_module/orm_sample_1.html', context)

'''  ==========================================================
part 2 select filter / where
 ========================================================== '''
def orm_sample_1_(request):
  routine_name  = 'orm_sample_1.html / filter , using Q'
  students = Student.objects.filter(classroom=2)
  # sample filter 1
  students = Student.objects.filter(lastname__startswith = 'pine' )| Student.objects.filter(lastname__startswith = 'latvo')
  # using Q onject
  # sample filter 2
  
  students = Student.objects.filter( 
    Q(lastname__startswith = 'pine') | 
    Q(lastname__startswith = 'latvo')
    )
  # sample filter 3
  
  students = Student.objects.filter( 
    Q(lastname__startswith = 'pine') | 
    ~Q(lastname__startswith = 'latvo') |
    Q(lastname__startswith = 'q')  
    )

  myquery = students.query
  
  
  connection_query = connection.queries
  context={'routine_name':routine_name,
           'students': students,
           'myquery': myquery,
           'connection_query': connection_query
           }
   
  return render(request,'orm_module/orm_sample_1.html', context)

'''  ==========================================================
part 3  and query
 ========================================================== '''
def orm_sample_1(request):
  routine_name  = 'orm_sample_1.html / filter , using Q'

  students = Student.objects.filter( classroom = 2) &      Student.objects.filter( lastname__startswith = 'qui') 
  # sample filter 1
  students = Student.objects.filter(Q(lastname__startswith='qui') | Q(classroom=1) )
 

  myquery = students.query
  
  
  connection_query = connection.queries
  context={'routine_name':routine_name,
           'students': students,
           'myquery': myquery,
           'connection_query': connection_query
           }
   
  return render(request,'orm_module/orm_sample_1.html', context)
'''  ==========================================================
part 4 qury union  note : removes duplicate rows 

=========================== '''
def orm_query_union(request):
  routine_name  = 'orm_query_union.html / union-query'

  new_list =Student.objects.all().values_list('firstname').union(Teacher.objects.all().values_list('firstname'))

  # note : values returns data dictionary

  new_list =Student.objects.all().values('firstname').union(Teacher.objects.all().values('firstname'))

  print(f'----->> Students : \n {new_list}')
  for item in new_list:
    print(f'{item}\n')

  myquery = new_list.query
  
  
  connection_query = connection.queries
  context={'routine_name':routine_name,
           'connection_query': connection_query,

           'new_list': new_list,
           'myquery': myquery,
           }  
  return render(request,'orm_module/orm_query_union.html', context)


def orm_query_union_not(request):

  routine_name  = 'orm_query_union_not.html / union-query (not)'
  # new_list =Student.objects.exclude( age__lte=20 ) & Student.objects.exclude( firstname__startswith = 'pri' )
  # new_list =Student.objects.filter( firstname__icontains='ia' ) 
  # new_list =Student.objects.filter( ~Q(firstname__icontains='ia') ) 
  # new_list =Student.objects.filter( ~Q(age__gt='20') & Q(firstname__icontains='C')) 
  new_list =Student.objects.filter( ~Q(age__gt='20') & Q(firstname__icontains='C')).only('firstname','age') 

  # for RAW QUERIES
  new_list = Student.objects.all()
  new_list = Student.objects.raw("select * from orm_module_student where age > 18 ")
   # another form of sql
  
  sql="select * from orm_module_student "
  new_list = Student.objects.raw(sql)[:2]  

  print(f'---->>>> new_list: {new_list} ')

  myquery = '' #new_list.query  
  connection_query = connection.queries  

  context={'routine_name':routine_name,
           'connection_query': connection_query,

           'new_list': new_list,
           'myquery': myquery,
           }  

  return render(request,'orm_module/orm_query_union_not.html', context)


'''  ==========================================================
accessing direct sql

=========================== '''
def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
'''  ==========================================================
direct sql
=========================== '''

def orm_query_direct(request):
  routine_name  = 'orm_query_direct.html / direct query'
  cursor = connection.cursor()

  sql="select * from orm_module_student  where age < 18"
  cursor.execute(sql)
  new_list = dictfetchall(cursor)
  # for item in new_list:
  #   print(i.firstname)
  print(f' ---->>>>  newlist : {new_list}')

  connection_query = connection.queries  
  # myquery = new_list.query  
  context={'routine_name':routine_name,
           'connection_query': connection_query,

           'new_list': new_list,
          #  'myquery': myquery,
           }    
  return render(request,'orm_module/orm_query_direct.html', context)
'''  ==========================================================
model inheritance
=========================== '''
def orm_model_inheritance(request):

  routine_name  = 'orm_model_inheritance.html / Model Inheritance'  
  new_list = Student.objects.filter( age = 17)

  # myquery = new_list.query  
  connection_query = connection.queries  
  context={'routine_name':routine_name,
           'connection_query': connection_query,

           'new_list': new_list,
          #  'myquery': myquery,
           }  
  return render(request,'orm_module/orm_model_inheritance.html', context)

def product_all(request):
  routine_name ='Product all'
  # new_list = Product.objects.all().prefetch_related('book','cupboard')
  new_list = Product.objects.all().select_related('book','cupboard')
  connection_query = connection.queries  
  context={'routine_name':routine_name,
           'connection_query': connection_query,

           'new_list': new_list,
          #  'myquery': myquery,
           }  
  return render(request,'orm_module/product_all.html', context)

def polymorphic(request):
  routine_name ='polymorphic sample 1'
  '''create objects'''
  # poly1Project.objects.create(topic="Department Party")
  # poly1ArtProject.objects.create(topic="Painting with Tim", artist="T. Turner")
  # poly1ResearchProject.objects.create(topic="Swallow Aerodynamics", supervisor="Dr. Winter")

  ''' 
  Use instance_of or not_instance_of for narrowing the result to specific subtypes:
  >>> Project.objects.instance_of(ArtProject)
[ <ArtProject:      id 2, topic "Painting with Tim", artist "T. Turner"> ]
  '''

  '''
  >>> Project.objects.instance_of(ArtProject) | Project.objects.instance_of(ResearchProject)
[ <ArtProject:      id 2, topic "Painting with Tim", artist "T. Turner">,
  <ResearchProject: id 3, topic "Swallow Aerodynamics", supervisor "Dr. Winter"> ]
  '''

  '''
  Polymorphic filtering: Get all projects where Mr. Turner is involved as an artist or supervisor (note the three underscores):
  -----
  >>> Project.objects.filter(Q(ArtProject___artist='T. Turner') | Q(ResearchProject___supervisor='T. Turner'))
[ <ArtProject:      id 2, topic "Painting with Tim", artist "T. Turner">,
  <ResearchProject: id 4, topic "Color Use in Late Cubism", supervisor "T. Turner"> ]
  '''
  # return render(request,'orm_module/orm_polymorphic.html', context)
  return HttpResponse('ab')
