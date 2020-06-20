from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# Create your models here.
class Futsal(models.Model):
    name        = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    main_img    = models.ImageField(upload_to='Futsal')
    cover_img   = models.ImageField(upload_to='Cover')
    description = RichTextField()
    price       = models.PositiveIntegerField()
    slug        = models.SlugField(unique=True,blank=True,null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    # location
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('futsal-detail', kwargs={'slug':self.slug})
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Futsal.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug,num)
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug(self)
        return super().save(*args, **kwargs)



