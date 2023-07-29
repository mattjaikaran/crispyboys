from django.contrib import admin

from predictions.models import Bet, Prediction

admin.site.register(Prediction)
admin.site.register(Bet)