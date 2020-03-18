from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'report'
urlpatterns = [
    path('', views.home, name='home'),
    path('oauth_login/', views.oauth_login, name='oauth_login'),
    path('oauth_callback/', views.oauth_callback, name='oauth_callback'),
    path('tsinghua_auth_login/', views.tsinghua_auth_login, name='tsinghua_auth_login'),
    path('tsinghua_auth_callback/', views.tsinghua_auth_callback, name='tsinghua_auth_callback'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='report/logged_out.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('record/', views.record_list, name='record_list'),
    path('record/add/', views.record_detail, name='record_detail'),
    path('entry/', views.entry_list, name='entry_list'),
    path('entry/add/', views.entry_detail, name='entry_detail'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('entry/<int:entry_id>/delete/', views.entry_delete, name='entry_delete'),
    path('building/', views.building_list, name='building_list'),
    path('building/<uuid:building_uuid>/', views.building_detail, name='building_detail'),
    path('building/<uuid:building_uuid>/<date>/', views.building_detail, name='building_detail'),
]
