from django.db import models

class Scent(models.Model):
    fragrance = models.CharField(max_length=100)
