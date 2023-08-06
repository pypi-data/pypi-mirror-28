# -*- coding: utf-8 -*-
import logging
import requests
import sys

from django.apps import apps

from . import choices


logger = logging.getLogger(__name__)


def upload_issue_location(instance, filename):
    Issue = apps.get_model('github_issues.Issue')
    last_issue = Issue.objects.order_by('id').last()

    if last_issue:
        new_id = last_issue.id + 1
    else:
        new_id = 1

    return '{0}/{1}'.format(new_id, filename)


def sync_github_issues():
    """
    Accomplishes 2 things. Loops through issues:
        - Creates issues on GitHub if number is not set
        - Update status if it is different on GitHub
    """
    logger.info('Updating Issues')
    session = requests.Session()
    Issue = apps.get_model('github_issues.Issue')
    Tag = apps.get_model('user_activities.Tag')
    issues = Issue.objects.all()

    for issue in issues:

        # Update status from GitHub
        if issue.number:
            response = session.get(issue.github_url)
            if response.status_code != 200:
                err_msg = 'Issue: {0} could not be synced!\n\n'.format(issue.number)
                err_msg += 'Response code: {0}. Error message: {1}'.format(
                    response.status_code,
                    response.text,
                )
                logger.error(err_msg)

            data = response.json()
            state = data.get('state', None)
            labels = data.get('labels', [])

            if state:
                issue.status = getattr(choices.STATUS, state)

            if len(labels) > 0:
                for label in labels:
                    tag, created = Tag.objects.get_or_create(label=label['name'])
                    issue.tags.add(tag)

            issue.save()

        # POST issue to GitHub
        else:
            data = {
                "title": issue.title,
                "body": "{0}\n\nSubmitted by: {1}".format(issue.body, issue.user.username),
                "labels": [x.slug for x in issue.tags.all()],
            }
            response = session.post(issue.github_url, data)

            if response.status_code != 201:
                err_msg = 'Issue: {0} was not created\n\n'.format(issue.title)
                err_msg += 'Response code: {0}. Error message: {1}'.format(
                    response.status_code,
                    response.text,
                )
                logger.error(err_msg)

            data = response.json()

            issue.number = data['number']
            issue.save()
