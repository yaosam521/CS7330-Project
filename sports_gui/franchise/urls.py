from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('league/', views.league, name = 'league'),
    path('date/', views.date, name = 'date')
]