from django import template

register = template.Library()

@register.filter
def is_later_than(datetime1, datetime2):
    """
    Custom template filter to check if datetime1 is later than datetime2.
    """
    return datetime1 > datetime2