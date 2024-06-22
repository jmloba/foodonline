import json
from django.db import models
from accounts.models import User
from menu.models import Product_Menu
from vendor.models import Vendor

# Create your models here.

request_object =''

class Payment(models.Model):
  PAYMENT_METHOD =(
    ('PayPal', 'PayPal'),
    ('RazorPay','RazorPay'),('GCash','Gcash'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  transaction_id= models.CharField(max_length=100)
  paypal_transaction_id= models.CharField(max_length=100, null=True, blank=True)
  payment_method = models.CharField(choices=PAYMENT_METHOD,max_length=100)
  amount=models.CharField(max_length=10)
  status=models.CharField(max_length=100, blank=True, null=True)
  created_at = models.DateField(auto_now_add=True)
  def __str__(self):
    return self.transaction_id
  
class Order(models.Model):
  STATUS = (
    ('New','New'),
    ('Accepted','Accepted'),
    ('Completed','Completed'),
    ('Cancelled','Cancelled')
  )
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null = True, blank = True)
  order_number = models.CharField(max_length=30)

  vendors = models.ManyToManyField(Vendor,blank=True)

  
  # coming from billing address
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone = models.CharField(max_length=15, blank = True)
  email = models.CharField(max_length=50)
  address = models.CharField(max_length=200)
  country = models.CharField(max_length=15, blank = True)
  state = models.CharField(max_length=15, blank = True)
  city = models.CharField(max_length=50 )
  pin_code = models.CharField(max_length=10 )
  
  total = models.FloatField()
  tax_data= models.JSONField(blank=True, null = True,help_text="Data format:{'tax_type':{'tax_percentage':'tax_amount'}}")
  total_tax = models.FloatField()

  total_data =models.JSONField(blank=True, null = True)

  payment_method =  models.CharField(max_length=25 )
  status =  models.CharField(max_length=15, choices=STATUS , default='New')
  is_ordered = models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  #concatenate firstname and lastname
  def name(self):
    return f'{self.first_name} {self.last_name}'
  def __str__(self):
    return self.order_number
  
  def get_total_by_vendor(self):
    vendor = Vendor.objects.get(user=request_object.user)

    if self.total_data :
      total_data =json.loads(self.total_data)
      data = total_data.get(str(vendor.id))
      print(f'*** models *** {data}')
      subtotal = 0
      tax = 0
      tax_dict ={}
      tax_total=0
      for key, val in data.items():
        print(f'-->> key :{ key}, value : {val} ')
        
        subtotal += float(key)
        
        print(f'val before  : {val}')
        val= val.replace("'", '"')
        print(f'val after  : {val}')

        val=json.loads(val)
        print(f'val json loads  : {val}')

        tax_dict.update(val)
        print(f' type of subtotal {type(subtotal)}, tax_dict {tax_dict}')
        # calculate tax
        # {'VAT': {'8.00': '3.36'}, 'Salestax': {'3.00': '1.26'}}
       
        for i in val:
          for j in val[i]:
            print(val[i][j])
            tax_total+= float(val[i][j])
    grandtotal = subtotal +   tax_total 
    print(f'--->>>final data extract')
    print(f'data : {data}')
    print(f'tax_dict : {tax_dict}')
    print(f'total purchase:{subtotal }')
    print(f'tax_total : {tax_total}')
    print(f'--->>>grandtotal :{grandtotal}\n\n')    
    context={'subtotal':subtotal,
             'tax_dict':tax_dict,
             'tax_total':tax_total,
             'grandtotal':grandtotal

    }
            
        

    return context

  
class OrderedFood(models.Model) :
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  product_item = models.ForeignKey(Product_Menu, on_delete=models.CASCADE)
  quantity =  models.IntegerField()
  price = models.FloatField()
  amount = models.FloatField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.product_item.product_title





