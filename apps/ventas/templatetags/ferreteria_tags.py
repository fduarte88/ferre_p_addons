from django import template

register = template.Library()


@register.filter
def guaranies(value):
    """Format a number as Paraguayan Guaraníes: Gs. 1.500.000"""
    try:
        amount = int(round(float(value)))
        formatted = f'{amount:,}'.replace(',', '.')
        return f'Gs. {formatted}'
    except (ValueError, TypeError):
        return value
