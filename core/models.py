from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(("First Name"), max_length=50)
    last_name = models.CharField(("Last Name"), max_length=50)
    email = models.EmailField(max_length=100)
    correct_predictions = models.IntegerField(default=0)
    correct_bets = models.IntegerField(default=0)
    total_predictions = models.IntegerField(default=0)
    total_bets = models.IntegerField(default=0)
    total_earnings = models.IntegerField(default=0)
    
    @property
    def full_name(self):
        return '{self.first_name} + {self.last_name}'
    
    @property
    def prediction_score(self):
        if self.total_predictions == 0:
            return 0
        else:
            accuracy = (self.correct_predictions / self.total_predictions) * 100
            return round(accuracy, 2)
    
    @property
    def bet_score(self):
        if self.total_bets == 0:
            return 0
        else:
            accuracy = (self.correct_bets / self.total_bets) * 100
            return round(accuracy, 2)
    
