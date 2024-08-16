from django.db import models
from django.utils import timezone

class Directory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subdirectories')

    def __str__(self):
        return self.name

    @property
    def get_ancestors(self):
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name='files')
    owner = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def link(self):
        return self.url if self.url else self.file.url if self.file else None
        
