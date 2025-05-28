from rest_framework import serializers
from .models import Path, Point, Background
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = ['id', 'title', 'image']
        read_only_fields = fields

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'path', 'x', 'y', 'order']
        read_only_fields = ['id', 'path', 'order']

class PathSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    background = serializers.PrimaryKeyRelatedField(
        queryset=Background.objects.all()
    )
    background_details = BackgroundSerializer(source='background', read_only=True)
    
    class Meta:
        model = Path
        fields = ['id', 'user', 'title', 'background', 'background_details', 'points']
        read_only_fields = ['id', 'user', 'background_details' 'points']

class PathCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = ['title', 'background']

class PointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['x', 'y', 'order']

class BoardPointSerializer(serializers.Serializer):
    row = serializers.IntegerField()
    col = serializers.IntegerField()
    color = serializers.CharField(max_length=16)

class BoardPointsListSerializer(serializers.Serializer):
    points = BoardPointSerializer(many=True)
