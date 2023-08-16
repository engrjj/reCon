from django import template

register = template.Library()

@register.filter(name='format_thousands_separator')
def format_thousands_separator(value):
    try:
        value = float(value)
        return '{:,.2f}'.format(value)
    except (ValueError, TypeError):
        return value
    
