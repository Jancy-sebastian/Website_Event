# from attr import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token
from rest_framework.fields import CurrentUserDefault



class EventSerializer(serializers.ModelSerializer):
    start_dates = serializers.DateTimeField(source="start_date",format="%d-%m-%y")
    end_dates = serializers.DateTimeField(source="end_date",format="%d-%m-%y")
    start_time = serializers.DateTimeField(source="start_date",format="%H:%M %p")
    end_time = serializers.DateTimeField(source="end_date",format="%H:%M %p")
    

    class Meta:
        fields = ['id', 'title','image','description','location',"start_time","end_time",'start_dates','end_dates','categories','published','paid']
        model = EventDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['username','email','password']