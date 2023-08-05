from django import VERSION as DJANGO_VERSION
from django import template
from django.conf import settings
if DJANGO_VERSION[0] == 1 and DJANGO_VERSION[1] <= 9:
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, viewname, css_class=None, strict=None):
    """
    Renders the given CSS class if the request path matches the path of the view.
    :param context: The context where the tag was called. Used to access the request object.
    :param viewname: The name of the view (include namespaces if any).
    :param css_class: The CSS class to render.
    :param strict: If True, the tag will perform an exact match with the request path.
    :return:
    """
    if css_class is None:
        css_class = getattr(settings, 'ACTIVE_LINK_CSS_CLASS', 'active')

    if strict is None:
        strict = getattr(settings, 'ACTIVE_LINK_STRICT', False)

    request = context.get('request')
    if request is None:
        # Can't work without the request object.
        return ''
    path = reverse(viewname)
    if strict:
        active = request.path == path
    else:
        active = path in request.path
    if active:
        return css_class
    return ''
