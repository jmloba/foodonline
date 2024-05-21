from django.contrib import admin


from .models import Teacher, Student, ItemA,BaseItem, ItemB, ItemC, ItemD, Product, Book, Cupboard 


# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
  list_display = ['id','firstname', 'lastname']
  ordering=('firstname',)
  filter_horizontal =()
  list_filter =()
  fieldsets=()

class StudentAdmin(admin.ModelAdmin):
  list_display = ['id','firstname', 'lastname','classroom', 'age']  

  ordering=('firstname',)  
  filter_horizontal =()
  list_filter =()
  fieldsets=()

class  ItemA_Admin(admin.ModelAdmin):
  list_display=['id','title','content','created_at','updated_at']
  ordering=('id',)  
  filter_horizontal =()
  list_filter =()
  fieldsets=()

class  ItemB_Admin(admin.ModelAdmin):
  list_display=['id','title','file','created_at','updated_at']
  ordering=('id',)  
  filter_horizontal =()
  list_filter =()
  fieldsets=()
class  ItemC_Admin(admin.ModelAdmin):
  list_display=['id','title','file','created_at','updated_at']
  ordering=('id',)  
  filter_horizontal =()
  list_filter =()
  fieldsets=()  

class  ItemD_Admin(admin.ModelAdmin):
  list_display=['id','title','slug','created_at','updated_at']
  ordering=('slug',)  
  filter_horizontal =()
  list_filter =()
  fieldsets=()  

class ProductAdmin(admin.ModelAdmin):
  list_display=['id','title','description', 'slug','price','in_stock', 'is_active', 'created']
  ordering=('slug',)  
  filter_horizontal =()
  list_filter =()
  fieldsets=()  

class BookAdmin(admin.ModelAdmin):
  # list_display=['id','title','description','image','slug','price','in_stock','is_active','publisher','author' ]

  list_display=['id','title','publisher','author' ]
  list_editable =('author','publisher')

  ordering=('publisher',)  
  filter_horizontal =()
  list_filter =()

  fieldsets=()  

class CupboardAdmin(admin.ModelAdmin):
  list_display=['id','title', 'shelves','author' ]
  ordering=('title',)  
  list_editable =('shelves','author',)
 
  filter_horizontal =()
  list_filter =()
  fieldsets=()  



admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Student, StudentAdmin)

admin.site.register(ItemA, ItemA_Admin)
admin.site.register(ItemB, ItemB_Admin)
admin.site.register(ItemC, ItemC_Admin)
admin.site.register(ItemD, ItemD_Admin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Cupboard, CupboardAdmin)


