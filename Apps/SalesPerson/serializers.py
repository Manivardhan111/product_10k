from rest_framework import serializers
from .models import admin_salesPerson

class AdminSalesPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=admin_salesPerson
        fields="__all__"
