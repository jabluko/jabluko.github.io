from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Max

from .models import Path, Point, Background
from .serializers import PathSerializer, PointSerializer, BackgroundSerializer
from .permissions import IsOwner
from rest_framework.exceptions import PermissionDenied

class PathViewSet(viewsets.ModelViewSet):
    serializer_class = PathSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only paths owned by the authenticated user
        return Path.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the path with the authenticated user
        serializer.save(user=self.request.user)


class PointViewSet(viewsets.ModelViewSet):
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Ensure points belong to the authenticated user's paths
        path = get_object_or_404(Path, id=self.kwargs['path_pk'], user=self.request.user)
        return Point.objects.filter(path=path)

    def perform_create(self, serializer):
        # Automatically associate the point with the correct path
        path = get_object_or_404(Path, id=self.kwargs['path_pk'], user=self.request.user)
        # Automatically assign the next order if not provided
        max_order = Point.objects.filter(path=path).aggregate(Max('order'))['order__max'] or 0
        serializer.save(path=path, order=max_order + 1)