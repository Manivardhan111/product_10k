from rest_framework import serializers
from .models import intrestedStudent,registeredStudents

class intrestedStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=intrestedStudent
        fields = "__all__"


class registeredStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=registeredStudents
        fields=['id','name','email','mobile','is_registered','payment_status','qualification']
    