# -*- coding: utf-8 -*-
from django.db.models import CharField, TextField

import django_filters
from genomix.filters import DisplayChoiceFilter

from . import choices, models


class IssueFilter(django_filters.rest_framework.FilterSet):

    username = django_filters.CharFilter(
        name='user__username',
        lookup_expr='iexact',
    )
    status = DisplayChoiceFilter(choices=choices.STATUS)

    class Meta:
        model = models.Issue
        fields = [
            'repo',
            'number',
            'title',
            'body',
            'user',
            'tags',
            'priority',
            'status',
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }


class RepoFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = models.Repo
        fields = [
            'label',
            'description',
            'owner',
            'descriptive_name',
            'html_url',
            'api_url',
            'active',
        ]
        filter_overrides = {
            CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
