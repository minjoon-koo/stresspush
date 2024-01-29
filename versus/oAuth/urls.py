from django.urls import path

from . import views

from django.urls import re_path
from .views import register_by_access_token
from .views import ObtainAuthToken


app_name = 'oAuth'


urlpatterns = [
    path('', views.index),
    re_path(r'^register-by-token/(?P<backend>[^/]+)/$', register_by_access_token),
    path('get-token/', ObtainAuthToken.as_view()),
] 