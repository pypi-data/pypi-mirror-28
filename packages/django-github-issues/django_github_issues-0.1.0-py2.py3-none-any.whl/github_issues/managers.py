# -*- coding: utf-8 -*-
from django.db import models


class IssueQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('repo') \
            .select_related('user') \
            .select_related('priority') \
            .prefetch_related('tags') \
            .all()
