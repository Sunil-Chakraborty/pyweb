import django_filters
from django.db import models
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'eid': ['exact', 'icontains'],
            'ename': ['exact', 'icontains'],
            'eemail': ['exact', 'icontains'],
            'econtact': ['exact', 'icontains'],
        }
        filter_overrides = {
            models.ImageField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
        
        