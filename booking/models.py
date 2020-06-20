from django.db import models
import datetime
from django.contrib.auth.models import User
from futsalApp.models import Futsal

class Booking(models.Model):
    fullname  = models.CharField(max_length=100)
    phone     = models.PositiveIntegerField()
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    futsal    = models.ForeignKey(Futsal, on_delete=models.CASCADE)
    time      = models.TimeField()
    date      = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Booking of {} for {}'.format(self.user.username, self.futsal.name)
    
    def is_valid(self, *args, **kwargs):
        now = datetime.date.today()
        if now > self.date:
            return False
        return True
    
     

