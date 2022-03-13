from django.db import models

class Candle(models.Model):
    candle_name = models.CharField(max_length=100)
    scent = models.ForeignKey("candlecommapi.scent", on_delete=models.CASCADE, default=1)
    profile = models.ForeignKey("candlecommapi.profile", on_delete=models.DO_NOTHING)
    jar_color = models.ForeignKey("candlecommapi.jarcolor", on_delete=models.SET_NULL, null=True)
    upload = models.ForeignKey("candlecommapi.upload", on_delete=models.SET_NULL, null=True)