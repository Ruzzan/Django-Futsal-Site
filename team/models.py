from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
from futsalApp.models import Futsal
from django.db.models.signals import pre_save
# Create your models here.
class Team(models.Model):
    name   = models.CharField(max_length=100)
    admin  = models.ForeignKey(User, related_name='admin',on_delete=models.DO_NOTHING)
    logo   = models.ImageField(upload_to='Team', default='default.png')
    bio    = models.TextField()
    members = models.ManyToManyField(User, through='TeamMember')
    slug    = models.SlugField(unique=True,blank=True,null=True,max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Team.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        return super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('team-detail', kwargs={'slug':self.slug})

class TeamMember(models.Model):
    team = models.ForeignKey(Team, related_name='memberships',on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ('team', 'user')


def capitalize_name(sender, instance, *args, **kwargs):
    instance.name = instance.name.title()

pre_save.connect(capitalize_name, sender=Team)