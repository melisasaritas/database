# serializers.py
from rest_framework import serializers

class YourSerializer(serializers.Serializer):
    comments = serializers.IntegerField()
    likes = serializers.IntegerField()
