from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=100)
    drive_url = models.URLField()

    def __str__(self):
        return self.title