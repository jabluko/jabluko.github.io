from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('select-background/', views.select_background, name='select_background'),
    path('backgrounds/', views.background_show, name="background_show"),
    path('paths/', views.path_list, name='path_list'),
    path('paths/new/', views.path_create, name='path_create'),
    path('paths/<int:path_id>/', views.path_detail, name='path_detail'),
    path('paths/<int:path_id>/add_point/', views.point_add, name='point_add'),
    path('points/<int:point_id>/delete/', views.point_delete, name='point_delete'),
]
