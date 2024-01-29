from django.urls import path

from . import views

from django.urls import re_path
from .views import register_by_access_token


app_name = 'ddpush'


urlpatterns = [
    path('', views.index),
    path('log/', views.log),
    path('log/text/', views.log_text),
    path('log/json/', views.log_json),
    path('log/yaml/', views.log_yaml),
    path('log/file/', views.log_file),
     path('log/push/', views.log_file),
    re_path(r'^register-by-token/(?P<backend>[^/]+)/$', register_by_access_token),
] 