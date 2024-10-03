from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    """
    Custom template filter to replace 'old' with 'new' in the string.

    Usage: {{ value|replace:"old,new" }}
    """
    try:
        old, new = arg.split(',')
        return value.replace(old, new)
    except ValueError:
        return value 