from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('studio/', views.dashboard_login, name='dashboard_login'),
    path('studio/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('studio/dashboard/', views.dashboard_home, name='dashboard_home'),
    path('studio/settings/', views.settings_edit, name='dashboard_settings'),
    path('studio/posts/', views.post_manage, name='dashboard_posts'),
    path('studio/posts/create/', views.post_create, name='dashboard_post_create'),
    path('studio/posts/<int:pk>/edit/', views.post_edit, name='dashboard_post_edit'),
    path('studio/furniture/', views.furniture_manage, name='dashboard_furniture'),
    path('studio/furniture/create/', views.furniture_create, name='dashboard_furniture_create'),
    path('studio/furniture/<int:pk>/edit/', views.furniture_edit, name='dashboard_furniture_edit'),
    path('studio/projects/', views.project_manage, name='dashboard_projects'),
    path('studio/projects/create/', views.project_create, name='dashboard_project_create'),
    path('studio/projects/<int:pk>/edit/', views.project_edit, name='dashboard_project_edit'),
]
