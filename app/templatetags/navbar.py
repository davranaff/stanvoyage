from django import template
from app.models import Menu

register = template.Library()


@register.inclusion_tag('tags/navbar.html', takes_context=True, name="navbar")
def navbar(context) -> dict[str, any]:

    path = context.get('request').path.split('/')[-2]

    query = Menu.objects.filter(is_active=True, language__name=context['request'].LANGUAGE_CODE).first()

    return {
        'info': query,
        'path': path
    }


