from django import template
from app.models import Menu, Blog

register = template.Library()


@register.inclusion_tag('tags/footer.html', takes_context=True, name="footer")
def footer(context) -> dict[str, any]:

    query = Menu.objects.filter(is_active=True, language__name=context['request'].LANGUAGE_CODE).first()
    blogs = Blog.objects.order_by('created_at')[:2]

    return {
        'info': query,
        'blogs': blogs,
    }
