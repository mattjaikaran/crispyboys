from django.contrib import admin
from predictions.models import Bet, Prediction

class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "prediction_text", "prediction_type", "is_correct", "result")

class BetAdmin(admin.ModelAdmin):
    list_display = ("prediction", "stake", "winner")

admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Bet, BetAdmin)