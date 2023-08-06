# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _

from genomix.models import TimeStampedLabelModel
from model_utils.models import TimeStampedModel

from . import app_settings, choices, managers, utils


class Issue(TimeStampedModel):
    """GitHub Issue."""

    repo = models.ForeignKey(
        'github_issues.Repo',
        on_delete=models.CASCADE,
        related_name='issues',
    )
    number = models.PositiveIntegerField(blank=True, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='issues',
    )
    screenshot = models.ImageField(
        upload_to=utils.upload_issue_location,
        width_field='width_field',
        height_field='height_field',
        blank=True,
        null=True,
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    tags = models.ManyToManyField(
        'user_activities.Tag',
        related_name='tags_issues',
        blank=True,
    )
    priority = models.ForeignKey(
        'user_activities.Tag',
        on_delete=models.SET_NULL,
        related_name='priority_issues',
        blank=True,
        null=True,
    )
    status = models.PositiveSmallIntegerField(
        choices=choices.STATUS,
        default=choices.STATUS.open,
    )
    comments = GenericRelation('user_activities.Comment')
    user_activities = GenericRelation('user_activities.Activity')

    objects = managers.IssueQuerySet.as_manager()

    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')
        unique_together = ('repo', 'number')

    def __str__(self):
        return str(self.number)

    @property
    def github_url(self):
        return '{0}/repos/{1}/{2}/issues/{3}?access_token={4}'.format(
            app_settings.GITHUB_API_URL,
            self.repo.owner,
            self.repo.label,
            self.number,
            app_settings.GITHUB_ACCESS_TOKEN,
        )


class Repo(TimeStampedLabelModel):
    """GitHub Repo."""

    owner = models.CharField(max_length=75)
    descriptive_name = models.CharField(max_length=75)
    html_url = models.URLField(unique=True)
    api_url = models.URLField(unique=True)

    class Meta:
        verbose_name = _('Repo')
        verbose_name_plural = _('Repos')
