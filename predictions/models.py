from django.db import models
from core.models import CustomUser


class Prediction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="prediction_user")
    prediction_type = models.CharField(max_length=50)
    prediction_text = models.TextField(max_length=1024)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'Prediction: {self.prediction_text} {self.prediction_type} - {self.user}'

class Bet(models.Model):
    users = models.ManyToManyField(CustomUser)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name="prediction_bet")
    stake = models.DecimalField(max_digits=8, decimal_places=2)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="winner_bet")
    
    def __str__(self):
        return f'Bet: {self.prediction}: {self.stake} - {self.winner}'
