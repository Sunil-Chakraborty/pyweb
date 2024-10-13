import django_filters
from django_filters import rest_framework as filters
from .models import Recepi

class RecepiFilter(filters.FilterSet):
    # Use the related model field for filtering
    comp_cd = filters.CharFilter(field_name='comp_cd__comp_cd', lookup_expr='icontains')
    rm_cd = filters.CharFilter(field_name='rm_cd__rm_cd', lookup_expr='icontains')
    
    class Meta:
        model = Recepi
        fields = {
            'comp_cd': ['exact', 'icontains'],
            'rm_cd': ['exact', 'icontains'],
        }
