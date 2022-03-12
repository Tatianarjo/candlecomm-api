from django.db import models

class Upload(models.Model):
    file_url = models.FileField(upload_to="photos/%Y/%m/%d/")
    