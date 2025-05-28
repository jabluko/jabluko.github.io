from django.urls import path

from . import views

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('select-background/', views.select_background, name='select_background'),
    path('backgrounds/', views.background_show, name="background_show"),
    
    path('home/', views.home, name='home'),

    path('paths/', views.path_list, name='path_list'),
    path('paths/new/', views.path_create, name='path_create'),
    path('paths/<int:path_id>/', views.path_detail, name='path_detail'),
    path('paths/<int:path_id>/add_point/', views.point_add, name='point_add'),
    path('points/<int:point_id>/delete/', views.point_delete, name='point_delete'),
    path('paths/<int:route_id>/delete/', views.delete_path, name='delete_path'),
    path('register/', views.register, name='register'),

    path('boards/', views.board_list, name='board_list'),
    path('boards/new/', views.board_create, name='board_create'),
    path('boards/<int:board_id>/', views.board_detail, name='board_detail'),

    path('allboards/', views.all_boards, name='allboard_list'),
    path('board_draw/<int:board_id>', views.board_draw, name='board_draw'),
]
