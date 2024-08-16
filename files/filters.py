# filters.py
import django_filters
from django.db import models
from .models import File

class FileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    url = django_filters.CharFilter(lookup_expr='icontains')
    # Add more fields if needed

    class Meta:
        model = File
        fields = ['name', 'url', 'directory']  # Specify the fields you want to filter by
        