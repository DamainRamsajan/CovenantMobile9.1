from django import template

register = template.Library()

@register.simple_tag
def nav_active(request_path: str, starts: str) -> str:
    """
    Return 'active' if the current path starts with the given prefix.
    Usage in a template:
        {% nav_active request.path '/dashboard' %}
    """
    return "active" if request_path.startswith(starts) else ""

