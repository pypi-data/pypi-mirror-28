# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import ConditionalPluginModel


class ConditionalContainerPlugin(CMSPluginBase):
    name = _(u'Conditional content')
    model = ConditionalPluginModel
    allow_children = True
    cache = False
    render_template = 'djangocms_conditional/conditional.html'

    def render(self, context, instance, placeholder):
        # Obtain user
        user = None
        if hasattr(context, 'request') and hasattr(context.request, 'user'):
            user = context.request.user
        if 'user' in context:
            user = context['user']
        if user and user.groups.filter(id=instance.permitted_group.id).exists():
            context['instance'] = instance

        return context

plugin_pool.register_plugin(ConditionalContainerPlugin)
