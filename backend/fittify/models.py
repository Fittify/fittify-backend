from django.db import models
import string
import random
from django.contrib.auth.models import User
from datetime import date

def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase), k = length)
        if Lobby.objects.filter(code = code).count() == 0:
            break
        return code
# Create your models here.
class Lobby(models.Model):
       ## unique Code for the Lobby
    code = models.CharField(max_length = 8, default = '', unique = True) 
    host = models.CharField(max_length= 50, unique = True)
    title = models.CharField(max_length=50, default = "Sport")
    sport = models.CharField(max_length=20)
    players = models.ManyToManyField(User)
    date_of_play = models.DateField(default = date.today)
    due_date = models.DateField()
    description =models.CharField(max_length = 500)
    max_number_of_players = models.IntegerField()
    place = models.CharField(max_length = 30)
    ## created_at = models.DateTimeField(auto_now_add = True)
