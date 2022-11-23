from django import template

register = template.Library()


@register.inclusion_tag("products/partials/boolean_icon.html")
def boolean_icon(boolean):
    return {'boolean': boolean}
