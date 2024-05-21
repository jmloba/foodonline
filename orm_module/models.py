from datetime import timezone
from django.db import models

# Create your models here.


class Teacher(models.Model):
  firstname = models.CharField(max_length=25)
  lastname = models.CharField(max_length=25)
  employee_id = models.IntegerField( unique=True)
  
  def __str__(self) :
    return self.firstname
  
class Student(models.Model):  
  firstname = models.CharField(max_length=25)
  lastname = models.CharField(max_length=25)
  email = models.EmailField(max_length=50)
  age = models.IntegerField()
  classroom = models.IntegerField()

  def __str__(self) :
    return self.firstname
  

class Books(models.Model):  
  title = models.CharField(max_length= 250)
  created= models.DateTimeField(auto_now_add=True)
  updated= models.DateTimeField(auto_now=True)

class  ISBN(Books):
  books_ptr = models.OneToOneField(
    Books,

    on_delete = models.CASCADE,
    parent_link = True,
    primary_key = True
  )
  ISBN = models.TextField()

class BookContent(models.Model):
  title= models.CharField(max_length=100)
  created = models.DateTimeField(auto_now_add=True)

class BookOrders(BookContent):
  class Meta:
    proxy = True
    ordering = ['created']

  def created(self):
    return timezone.now() - self.created_at


  
class BaseItem(models.Model):  
  title = models.CharField(max_length= 250)
  created_at= models.DateTimeField(auto_now_add=True)
  updated_at= models.DateTimeField(auto_now=True)

  class Meta:
    abstract=True
    ordering = ['title']

class ItemA(BaseItem) :   
  content=models.TextField()

  class Meta(BaseItem.Meta):
    ordering =['-created_at']



class ItemB(BaseItem) :   
  file=models.FileField(upload_to='files')

class ItemC(BaseItem) :   
  file=models.FileField(upload_to='images')  

class ItemD(BaseItem) :   
  slug=models.SlugField(max_length=250,unique=True)

class Product(models.Model):
  title       = models.CharField(max_length =255)
  description = models.TextField(blank = True)
  image       = models.ImageField(upload_to='images/book/', default='images/book/default.png')
  slug        = models.SlugField(max_length=255)
  price       = models.DecimalField(max_digits=4, decimal_places=2)
  in_stock  = models.BooleanField(default=True)
  is_active = models.BooleanField(default = True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now= True)
  class Meta:
    ordering = ('-created',)

class Book(Product):
  publisher = models.CharField(max_length = 255)
  author = models.CharField(max_length =255)

class Cupboard(Product):
  shelves = models.IntegerField()
  author = models.CharField(max_length=255)



