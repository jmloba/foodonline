from .models import Cart, Tax
from menu.models import Product_Menu

def get_cart_counter(request):
  # print(f'context processor : get_cart_counter ')
  cart_count=0
  if request.user.is_authenticated:
    try:
      cart_items = Cart.objects.filter(user=request.user)
      if cart_items:
        for cart_item in cart_items:
          cart_count += cart_item.quantity
      else:
        cart_count = 0

    except:
      cart_count = 0
      
  return dict(cart_count=cart_count)

def get_cart_amount(request):
  # print(f'context processor :  get_cart_amount ')  
  subtotal = 0
  tax =0
  grand_total =0
  tax_dict ={}
  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
      product_item = Product_Menu.objects.get(pk=item.product_item.id)
      subtotal += (product_item.price * item.quantity)

    get_tax = Tax.objects.filter(is_active = True)
    # print(f'get tax , {get_tax}')
    for i in get_tax:
      tax_type = i.tax_type
      tax_percentage = i.tax_percentage
      tax_amount = round((tax_percentage * subtotal)/100,2)
      print(f'marketplace->context_processor***-->>>tax_type :{tax_type}, tax_percentag:{tax_percentage},tax_amount : {tax_amount} ')
      '''
          note :   we need a dictionary as :
          re : Taxes are  SalesTax, VAT
          {'Sales Tax':{'3.0':'9:42'}, 'VAT':{'8.0':'25.12'}}
      '''
      tax_dict.update({tax_type: {str(tax_percentage):tax_amount}})

    tax=0

    # for key in tax_dict.values():
    #   for x in key.values():
    #     tax +=x

    tax =sum(x for key in tax_dict.values() for x in key.values() )    
    
    grand_total = subtotal + tax 

    # print(f'tax dictionary : {tax_dict}')
    # print(f'tax  : {tax}')
    # print (f'printed from context processor called when adding and subtracting quantity')

    # print(f' subtotal : {subtotal}, grand total :{grand_total}')
  return dict(subtotal=subtotal,tax=tax,grand_total=grand_total, tax_dict=tax_dict)
