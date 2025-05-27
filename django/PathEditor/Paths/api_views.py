from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import *
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework.authtoken.models import Token

from .models import Path, Point, Background
from .serializers import PathSerializer, PointSerializer, BackgroundSerializer
from .permissions import IsOwner
from rest_framework.exceptions import PermissionDenied

class PathViewSet(viewsets.ModelViewSet):
    serializer_class = PathSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Path.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PointViewSet(viewsets.ModelViewSet):
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        path = get_object_or_404(Path, id=self.kwargs['path_pk'], user=self.request.user)
        return Point.objects.filter(path=path)

    def perform_create(self, serializer):
        path = get_object_or_404(Path, id=self.kwargs['path_pk'], user=self.request.user)
        max_order = Point.objects.filter(path=path).aggregate(Max('order'))['order__max'] or 0
        serializer.save(path=path, order=max_order + 1)

@api_view(['GET'])
@login_required
def get_user_token(request):
    token, created = Token.objects.get_or_create(user=request.user)
    return Response({'token': token.key})