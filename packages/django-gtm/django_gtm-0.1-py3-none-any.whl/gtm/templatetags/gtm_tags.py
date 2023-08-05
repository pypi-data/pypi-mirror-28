from django import template
from django.conf import settings

from .. models import GTMDefault, GTMSettings


register = template.Library()


@register.inclusion_tag('gtm/gtm.html', name='gtm')
@register.inclusion_tag('gtm/gtm_head.html', name='gtm_head')
@register.inclusion_tag('gtm/gtm_body.html', name='gtm_body')
def gtm_tag(google_tag_id=None, *args, **kwargs):
    if google_tag_id:
        return {'gtm_id': google_tag_id}

    name = kwargs.get('name')
    if not name:
        code = GTMDefault.load().code
    else:
        container = GTMSettings.objects.filter(name=name).first()
        code = container.code if container else GTMDefault.load().code
    return {'gtm_id': code}
