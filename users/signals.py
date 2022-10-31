from django.db.models.signals import post_save #this method gets fired when object is created
from django.contrib.auth.models import User #we want signal when User is created
from django.dispatch import receiver #function that gets signal and performs task
from .models import Profile #we will be creating a profile in function



@receiver(post_save,sender=User) #when user is saved send this signal
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()