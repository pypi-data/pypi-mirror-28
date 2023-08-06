# -*- coding: utf-8
from django.contrib import admin

from . import models


class IssueAdmin(admin.ModelAdmin):
    model = models.Issue
    list_display = ('repo', 'number', 'title', 'user', 'status', 'created', 'modified')
    raw_id_fields = ('repo', 'user', 'tags', 'priority')
    search_fields = ('title', 'body')
    list_filter = ('tags', 'priority', 'status')
    save_as = True


class RepoAdmin(admin.ModelAdmin):
    model = models.Repo
    list_display = ('label', 'owner', 'descriptive_name', 'active', 'created', 'modified')
    prepopulated_fields = {'slug': ('label', )}
    search_fields = ('label', 'description', 'owner', 'descriptive_name')
    list_filter = ('active', )
    save_as = True


admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.Repo, RepoAdmin)
