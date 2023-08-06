# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


STATUS = Choices(
    (1, 'open', _('open')),
    (2, 'closed', _('closed')),
)
