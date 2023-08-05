from django.core.urlresolvers import resolve, reverse
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import checkout_flow_steps

from .frontend import MabelStep


@receiver(checkout_flow_steps, dispatch_uid="mabel_checkout_step")
def mabel_checkout_step(sender, **kwargs):
    return MabelStep


@receiver(nav_event_settings, dispatch_uid='mabel_settings')
def mabel_settings(sender, request, **kwargs):
    print(request.path_info)
    url = resolve(request.path_info)
    return [{
        'label': _('Mabel Settings'),
        'url': reverse('plugins:pretix_mabel:settings', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_mabel' and url.url_name == 'settings',
    }]
