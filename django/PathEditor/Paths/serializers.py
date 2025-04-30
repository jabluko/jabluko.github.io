from rest_framework import serializers
from .models import Route, RoutePoint, BackgroundImage
from django.contrib.auth.models import User

class BackgroundSerializer(serializers.ModelSerializer):
    """Prosty serializer do wyświetlania info o tle w trasie."""
    class Meta:
        model = BackgroundImage
        fields = ['id', 'name', 'image']
        read_only_fields = fields

class RoutePointSerializer(serializers.ModelSerializer):
    """Serializer dla punktów trasy."""
    route = serializers.PrimaryKeyRelatedField(read_only=True)
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoutePoint
        fields = ['id', 'route', 'x', 'y', 'order']
        read_only_fields = ['id', 'route', 'order']

class RouteSerializer(serializers.ModelSerializer):
    """Serializer dla tras."""
    owner = serializers.ReadOnlyField(source='owner.username')
    points = RoutePointSerializer(many=True, read_only=True)
    background_image = serializers.PrimaryKeyRelatedField(
        queryset=BackgroundImage.objects.filter(is_active=True)
    )
    background_image_details = BackgroundSerializer(source='background_image', read_only=True)


    class Meta:
        model = Route
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'background_image', # Pole do zapisu (ID)
            'background_image_details', # Pole do odczytu (szczegóły)
            'created_at',
            'updated_at',
            'points', # Lista punktów (tylko do odczytu)
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'points', 'background_image_details']

    def validate_background_image(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Wybrany obraz tła jest nieaktywny.")
        return value
