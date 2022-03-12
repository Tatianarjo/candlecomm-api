from django.db import models

class DiscussionBoard(models.Model):
    profile = models.ForeignKey("candlecommapi.Profile", on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=140)
    message = models.CharField(max_length=500)