# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class ConditionalPluginModel(CMSPlugin):

    permitted_group = models.ForeignKey(Group, null=False, blank=False)

    def __str__(self):
        return _(u'Access granted to members of %s') % self.permitted_group.name
