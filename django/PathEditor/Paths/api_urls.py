from rest_framework_nested import routers
from . import api_views

# Main router for paths
paths_router = routers.SimpleRouter()
paths_router.register(r'paths', api_views.PathViewSet, basename='path')

points_nested_router = routers.NestedSimpleRouter(paths_router, r'paths', lookup='path')
points_nested_router.register(r'points', api_views.PointViewSet, basename='points')

urlpatterns = paths_router.urls + points_nested_router.urls