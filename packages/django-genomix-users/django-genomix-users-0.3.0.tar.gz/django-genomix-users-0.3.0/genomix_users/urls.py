# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from rest_framework import routers
from rest_framework_jwt import views as jwt_views

from . import viewsets


router = routers.SimpleRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'user-profiles', viewsets.ProfileViewSet)

default_router = routers.DefaultRouter()
default_router.register(r'users', viewsets.UserViewSet)
default_router.register(r'user-profiles', viewsets.ProfileViewSet)

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', jwt_views.obtain_jwt_token),
    url(r'^api-token-refresh/', jwt_views.refresh_jwt_token),
    url(r'^api-token-verify/', jwt_views.verify_jwt_token),
] + router.urls
