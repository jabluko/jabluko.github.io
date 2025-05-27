from django.urls import path
from rest_framework_nested import routers
from . import api_views

paths_router = routers.SimpleRouter()
paths_router.register(r'paths', api_views.PathViewSet, basename='path')

points_nested_router = routers.NestedSimpleRouter(paths_router, r'paths', lookup='path')
points_nested_router.register(r'points', api_views.PointViewSet, basename='points')

urlpatterns = paths_router.urls + points_nested_router.urls + [
    path('my-token/', api_views.get_user_token, name='get_user_token'),
]
