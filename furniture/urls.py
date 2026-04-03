from django.urls import path
from . import views
urlpatterns = [path('', views.furniture_list, name='furniture_list'), path('<slug:slug>/', views.furniture_detail, name='furniture_detail')]
