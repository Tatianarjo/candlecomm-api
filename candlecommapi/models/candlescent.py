from django.db import models

class CandleScent(models.Model):
    candle = models.ForeignKey("candlecommapi.Candle", on_delete=models.SET_NULL, null=True)
    scent = models.ForeignKey("candlecommapi.Scent", on_delete=models.SET_NULL, null=True)