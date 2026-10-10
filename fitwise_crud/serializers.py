from django.contrib.auth.models import User
from rest_framework import serializers 
from fitwise_crud.models import Foodlog

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

class FoodSerializer(serializers.ModelSerializer):

    class Meta:

        model = Foodlog
        fields="__all__"
        read_only_fields=["id","owner","created_at"]
