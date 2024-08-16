
from django.db import models

import os



def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.eid), filename)

class Employee(models.Model):
    eid = models.CharField(max_length=20)
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    econtact = models.CharField(max_length=250)
    prof_image = models.ImageField(verbose_name='Attachment(image)', upload_to=get_image_path, null=True, blank=True)

    class Meta:
        db_table = "employee"

