from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from PIL import Image
from futsalApp.models import Futsal
# Create your models here.

class Profile(models.Model):
    user       = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar     = models.ImageField(default='default.png', upload_to='Profile')
    favourites = models.ManyToManyField(Futsal,blank=True,null=True)
    is_owner   = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)
    
    # def get_absolute_url(self):
    #     return reverse('profile', kwargs={'username':self.user.username})

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            outputSize = (300,300)
            img.thumbnail(outputSize)
            img.save(self.avatar.path)
    
def profile_create(sender, instance, created ,*args, **kwargs):
    if created:
        Profile.objects.create(user = instance)

def profile_save(instance, *args, **kwargs):
    instance.profile.save()

post_save.connect(profile_create, sender=User)
post_save.connect(profile_save, sender=User)

    

    
