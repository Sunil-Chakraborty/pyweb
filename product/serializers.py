from rest_framework import serializers
from .models import Recepi

class RecepiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recepi
        fields = '__all__'
