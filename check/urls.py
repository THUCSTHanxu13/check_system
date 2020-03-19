from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'check'

urlpatterns = [
    path('index/', views.index, name='check_index'),
    path('upload/', views.upload, name='check_upload'),
    path('wait/', views.wait, name='check_wait'),
    path('download/<str:uid>/', views.download, name='check_download'),
    url(r'^spider/download/(?P<filename>.+)$', views.getfile, name='getfile'),
]


