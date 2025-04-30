from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Max

from .models import Path, Point, Background
from .serializers import PathSerializer, PathSerializer, BackgroundSerializer
from .permissions import IsOwner
from rest_framework.exceptions import PermissionDenied

@api_view(['GET'])
def get_backgrounds(request, background_id):
    bg = Background.objects.get(id=background_id)
    return Response(BackgroundSerializer(bg).data)


class PathViewSet(viewsets.ModelViewSet):
    serializer_class = PathSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Path.objects.filter(user=self.request.user).prefetch_related('points', 'background_image')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PathViewSet(viewsets.ModelViewSet):
    serializer_class = PathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        path_id = self.kwargs.get('path_id')
        
        if getattr(self, 'swagger_fake_view', False):
            return Path.objects.none()
        path = get_object_or_404(Path, id=path_id, user=self.request.user)
        return Path.objects.filter(path=path).order_by('order')

    def perform_create(self, serializer):
        path_id = self.kwargs.get('path_id')
        path = get_object_or_404(path, id=path_id, user=self.request.user)

        last_point_order = path.objects.filter(Path=path).aggregate(Max('order'))['order__max']
        next_order = (last_point_order or 0) + 1

        serializer.save(Path=path, order=next_order)

    def perform_update(self, serializer):
        point = serializer.instance
        if point.path.user != self.request.user:
            raise permissions.PermissionDenied("Nie masz uprawnień do modyfikacji punktów tej trasy.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.path.user != self.request.user:
            raise permissions.PermissionDenied("Nie masz uprawnień do usuwania punktów tej trasy.")
        instance.delete()
