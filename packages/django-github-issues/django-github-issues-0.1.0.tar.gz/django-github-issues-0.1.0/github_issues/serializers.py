# -*- coding: utf-8 -*-
from django.apps import apps

from genomix.fields import DisplayChoiceField, UserRelatedField
from rest_framework import serializers

from . import choices, models


Tag = apps.get_model('user_activities.Tag')


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for viewing GitHub Issues."""

    user = UserRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='slug',
        many=True,
    )
    priority = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='slug',
    )
    status = DisplayChoiceField(choices=choices.STATUS)

    class Meta:
        model = models.Issue
        fields = (
            'id', 'repo', 'number', 'title', 'body', 'user',
            'screenshot', 'tags', 'priority', 'status',
            'created', 'modified',
        )


class RepoSerializer(serializers.ModelSerializer):
    """Serializer for viewing GitHub Repos."""

    class Meta:
        model = models.Repo
        fields = (
            'id', 'label', 'description',
            'owner', 'descriptive_name', 'html_url', 'api_url',
            'active', 'created', 'modified',
        )
