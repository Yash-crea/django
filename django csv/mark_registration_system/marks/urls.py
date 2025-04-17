from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('input_mark/', views.input_mark, name='input_mark'),
    path('view_mark/', views.view_mark, name='view_mark'),
    path('update_mark/', views.update_mark, name='update_mark'),
    path('visualisation/', views.visualisation, name='visualisation'),
]
