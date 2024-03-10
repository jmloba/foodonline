from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile 

from .models import User

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance,created,**kwargs):
  print(f'*****   --->>>>>>  s i g n a l  : user created {created}')

  if created :
    UserProfile.objects.create(user=instance)
    print(f'*****   --->>>>>>  s i g n a l  : user profile is created')
  else  :
    try:
      print(f'*****   --->>>>>>  s i g n a l  : user profile is only updated')
      profile = UserProfile.objects.get(user=instance)
      profile.save()
    except:
      #create the user profile if not exist  
      UserProfile.objects.create(user=instance)
      print(f"user profile does not exist but created one... {instance} is created")

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance,**kwargs):
  print(instance.username,'-- pre--save this user is being saved')
  # post_save.connect(post_save_create_profile_receiver,sender=User)