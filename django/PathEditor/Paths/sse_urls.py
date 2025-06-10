from django.urls import path
from . import sse_views

urlpatterns = [
    path('notifications/', sse_views.sse_notifications, name='sse_notifications'),
]
