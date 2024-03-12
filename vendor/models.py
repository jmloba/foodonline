from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification


# Create your models here.
class Vendor(models.Model):
  user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
  user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
  vendor_name = models.CharField(max_length=75)
  vendor_license= models.ImageField(upload_to='vendor/license')
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.vendor_name
  
  def save(self,*args,**kwargs):
    if self.pk is not None:
      #update
      orig = Vendor.objects.get(pk=self.pk) # get the original status of vendor
      if orig.is_approved != self.is_approved:
        mail_template = 'accounts/email/admin_approval_email.html'
        context ={'user': self.user, 'is_approved': self.is_approved,}
        if self.is_approved == True:
          # send notification email
          mail_subject = 'Congratulations, your restaurant/Vendor has been approved !!!'
          send_notification(mail_subject, mail_template, context)
        
        else :
          # send notification
          mail_subject = 'Sorry you are not eligible in publishing your product on the market place'
          send_notification(mail_subject, mail_template, context)
    else:
      print('vendor save .. no pk available')
      


    return super(Vendor,self).save(*args,**kwargs)
