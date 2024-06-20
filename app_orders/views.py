from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
# Create your views here.
from marketplace.models import Cart
from marketplace.context_processor import get_cart_amount
from app_orders.forms import OrderForm
from app_orders.models import Order,Payment, OrderedFood
import simplejson as json
from app_orders.utils import generate_order_number
from accounts.utils import send_notification,reformat_date
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def place_order(request) :
  cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
  cart_count=cart_items.count()
  if cart_count <=0 :
    return redirect('marketplace:marketplace')
  
  # get from marketplace -> context processor
  subtotal= get_cart_amount(request)['subtotal']
  total_tax= get_cart_amount(request)['tax']
  grand_total= get_cart_amount(request)['grand_total']
  tax_dict= get_cart_amount(request)['tax_dict']

  if request.method=='POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      # form.save()
      order=Order()
      order.user = request.user
      order.first_name= form.cleaned_data['first_name']
      order.last_name = form.cleaned_data['last_name'] 
      order.phone = form.cleaned_data['phone']
      order.email = form.cleaned_data['email']
      order.address = form.cleaned_data['address']
      order.country = form.cleaned_data['country']
      order.state = form.cleaned_data['state']
      order.city = form.cleaned_data['city']
      order.pin_code = form.cleaned_data['pin_code']
      
      order.total = grand_total
      order.tax_data =json.dumps(tax_dict)
      order.total_tax = total_tax
      order.payment_method = request.POST['payment_method']
      order.save()
      
      order.order_number = generate_order_number(order.id)
      order.save()
      
      context = {'cart_items': cart_items, 'order': order,
             'subtotal':subtotal,
             'grand_total': grand_total,
             'tax_dict' : tax_dict,
             'total_tax': total_tax,
             'order_number' : order.order_number
             }
      return render(request,'app_orders/place-order.html', context)

      
    else :
      print(f'form.errors -->>> {form.errors}')
    

  context = {'cart_items': cart_items, 
             'subtotal':subtotal,
             'grand_total': grand_total,
             'tax_dict' : tax_dict,
             'total_tax': total_tax,
             }
  return render(request,'app_orders/place-order.html', context)


def send_to_email(request, cart_items, order) :
    #send email
    mail_subject = 'Your Orders has been processed'
    mail_template = 'accounts/email/payment_notification.html'
    
    context = {'user':request.user, 'order':order,'to_email':order.email}

    send_notification(mail_subject, mail_template, context)

    # send order received to the vendor     
    print(f'sending notification to vendors')
    mail_subject = 'You have a new order'
    mail_template = 'accounts/email/vendor_notification.html'
    to_emails =[]
    for i in cart_items:
      if i.product_item.vendor.user.email not in to_emails:
        to_emails.append(i.product_item.vendor.user.email)
    print(f'to emails : {to_emails}')    

    context = {'user':request.user, 'order':order,'to_email':to_emails}
    send_notification(mail_subject, mail_template, context)    


@login_required(login_url='login')
def save_to_payment(request):
  # check if request is ajax or not
  if request.headers.get('x-requested-with')=='XMLHttpRequest' and request.method=='POST':
    # store the payment details in the payment model  
    order_number = request.POST.get('order_number')
    transaction_id = request.POST.get('transaction_id')
    payment_method = request.POST.get('payment_method')
    grand_total = request.POST.get('grand_total')
    status = request.POST.get('status')
    paypal_transaction_id = request.POST.get('paypal_transaction_id')

    print(f'\n\n before saving : order number  :{order_number}\n transaction_id :{transaction_id}\npayment Method : {payment_method}\nstatus : {status} ')
    
    order =Order.objects.get(user = request.user, order_number=order_number )
    payment=Payment(
      user=request.user,
      transaction_id=transaction_id,
      payment_method= payment_method,

      amount=order.total,
      paypal_transaction_id=paypal_transaction_id

    )
    payment.save()
    # update order model
    order.payment = payment
    order.is_ordered=True
    order.save()

    # move cart items to ordered foods
    cart_items = Cart.objects.filter(user = request.user)
    cart_list= list(cart_items
               )
    
    print(f'list cart_items : {cart_items}' )

    for item in cart_items:
      ordered_food = OrderedFood()
      ordered_food.order=order
      ordered_food.payment = payment
      ordered_food.user = request.user
      ordered_food.product_item= item.product_item
      ordered_food.quantity = item.quantity
      ordered_food.price = item.product_item.price
      # total amount
      ordered_food.amount = item.product_item.price * item.quantity
      ordered_food.save()



    # joven- uncomment these sending emails *** daily limit email
    # send_to_email(request, cart_items, order)

    #clear cart
    cart_items.delete()
    response={'status':'Success',
              'order_status':'Order has been accepted',
              'order_number': order_number,
              'transaction_id': transaction_id
          
              }
    return JsonResponse(response)
  return JsonResponse({'status':'Success','message':'save to payment ok'})

def order_complete(request)  :
  order_number = request.GET.get('order_no')
  transaction_id = request.GET.get('trans_id')

  try:
    order=Order.objects.get(order_number=order_number, payment__transaction_id= transaction_id, is_ordered=True) 
    ordered_food =OrderedFood.objects.filter(order=order)
    ''' other way to get the totals, tax_data'''
    subtotal = 0
    for item in ordered_food:
      subtotal += (item.quantity * item.price)
    # loading tax data
    tax_data = json.loads(order.tax_data)  



    context={'order_number':order_number, 'transaction_id':transaction_id, 
    'order':order,
    'ordered_food':ordered_food,
    'subtotal':subtotal,
    'tax_data':tax_data
    }
    return render(request, 'app_orders/order-complete2.html',context)
    
  except:
    return redirect('home')


