#predictn urls

from django.urls import include, path

from . import views

from predictn.models import n_data



urlpatterns = [
    path('', views.index),
    path('<str:course_num>/', views.course, name='results')
    ]
    

