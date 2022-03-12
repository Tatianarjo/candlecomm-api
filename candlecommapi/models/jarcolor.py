from django.db import models

class JarColor(models.Model):
    color = models.CharField(max_length=50)