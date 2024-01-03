from rest_framework import serializers
from .models import admin_salesPerson

class RegisterSalesPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=admin_salesPerson
        fields="__all__"
