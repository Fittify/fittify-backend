from django.db import models

from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Lobby(models.Model):
    title = models.CharField(max_length=50, default = "Sport")
    sport = models.CharField(max_length=20)
    players = models.ManyToManyField(User)
    date_of_play = models.DateField(default = date.today)
    due_date = models.DateField()
    description =models.CharField(max_length = 500)
    max_number_of_players = models.IntegerField()
    place = models.CharField(max_length = 30)
