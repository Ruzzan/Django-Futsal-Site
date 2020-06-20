from django.db import models
from django.contrib.auth.models import User
from futsalApp.models import Futsal
from team.models import Team
# Create your models here.
class Match(models.Model):
    futsal       = models.ForeignKey(Futsal, on_delete=models.CASCADE)
    team         = models.ForeignKey(Team, on_delete=models.CASCADE)
    date         = models.DateField()
    start_time   = models.TimeField()
    end_time     = models.TimeField()
    player_count = models.IntegerField(default=5)
    timestamp    = models.DateTimeField(auto_now_add=True)
    game_type    = models.CharField(max_length=100, choices=(
        ('f', 'Friendly'),
        ('l', 'Loser\'s Pay')
    ))

    def __str__(self):
        return "Match of {}".format(self.team.name)

class MatchObject(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return 'Match between {} and {}'.format(self.match.team,self.opponent)

