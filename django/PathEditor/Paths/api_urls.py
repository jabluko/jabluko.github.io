from rest_framework_nested import routers
from . import api_views

router = routers.SimpleRouter()
router.register(r'paths', api_views.PathViewSet, basename='route')
routes_router = routers.NestedSimpleRouter(router, r'paths', lookup='path')
routes_router.register(r'points', api_views.PathViewSet, basename='path-points')
urlpatterns = router.urls + routes_router.urls