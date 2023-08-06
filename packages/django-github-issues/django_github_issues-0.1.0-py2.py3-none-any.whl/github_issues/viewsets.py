# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from . import filters, models, serializers


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing GitHub Issues."""

    queryset = models.Issue.objects.fast()
    serializer_class = serializers.IssueSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = filters.IssueFilter
    search_fields = ('title', 'body')


class RepoViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing GitHub Repos."""

    queryset = models.Repo.objects.all()
    serializer_class = serializers.RepoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = filters.RepoFilter
    search_fields = ('label', 'description', 'descriptive_name')
