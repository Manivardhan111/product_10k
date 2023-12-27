from rest_framework import serializers
from .models import intrestedStudent

class intrestedStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=intrestedStudent
        fields = ['id', 'name', 'email', 'city', 'qualification','mobile']