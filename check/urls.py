from django.urls import path

from . import views

app_name = 'check'

urlpatterns = [
    path('index/', views.index, name='check_index'),
    path('upload/', views.upload, name='check_upload'),
]
