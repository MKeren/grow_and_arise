from django import template

register = template.Library()

@register.filter
def get_range(value):
    """Retourne un range basé sur la valeur."""
    return range(value)
