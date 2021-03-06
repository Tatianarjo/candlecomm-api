from django.db import models

class Vote(models.Model):
    like = models.BooleanField(default=False)
    candle = models.ForeignKey("candlecommapi.Candle", on_delete=models.DO_NOTHING)
    profile = models.ForeignKey("candlecommapi.Profile", on_delete=models.PROTECT)
