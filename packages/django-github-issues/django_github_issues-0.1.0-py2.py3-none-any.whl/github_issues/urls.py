# -*- coding: utf-8 -*-
from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter()
router.register(r'issues', viewsets.IssueViewSet)
router.register(r'repos', viewsets.RepoViewSet)

default_router = routers.DefaultRouter()
default_router.register(r'issues', viewsets.IssueViewSet)
default_router.register(r'repos', viewsets.RepoViewSet)


urlpatterns = default_router.urls
