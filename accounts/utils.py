from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
  if user.role == 1:
    redirectUrl ='dashboardVendor'
  elif  user.role == 2:
    redirectUrl ='dashboardCustomer'
  elif  user.role == None and user.is_superadmin:
    redirectUrl ='/admin'

  return redirectUrl





def send_verification_email(request,user,mail_subject,email_template):
  from_email = settings.DEFAULT_FROM_EMAIL
  current_site = get_current_site(request) 
  message =render_to_string(email_template,      
        {
        'user':user,
        'domain': current_site,
        # encode users primary key -> user.pk
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)      }
        )
  to_email = user.email
  mail = EmailMessage(mail_subject,message, to=[to_email])
  #sending email in html format
  mail.content_subtype = 'html'
  
  mail.send()


# called form vendor models
def send_notification(mail_subject, mail_template, context):
  from_email = settings.DEFAULT_FROM_EMAIL
  message =render_to_string(mail_template,     context )

  if (isinstance(context['to_email'],str)):
    to_email=[]
    to_email.append(context['to_email'])
  else:  
    to_email = context['to_email']
  mail = EmailMessage(mail_subject,message, to=to_email)
  mail.content_subtype = 'html'
  mail.send()

  return

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def reformat_date(val):
  print(f'reformatting val: {val}')
  #  abbreviated month %b
  #  abbreviated full month %B
  # val = val.strftime("%B %d, %Y, %H:%M ")
  # val = val.strftime("%B %d, %Y, %I:%M %p")
  val = val.strftime("%Y/%m/%d, %I:%M %p")
  return val

