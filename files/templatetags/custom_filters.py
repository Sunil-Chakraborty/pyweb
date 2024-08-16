from django import template

register = template.Library()

@register.filter
def replace(value, args):
    search, replace_with = args.split(',')
    return value.replace(search, replace_with)
"""
@register.filter
def endswith(value, suffix):
    
    if isinstance(value, str):
        return value.endswith(suffix)
    return False
"""
@register.filter
def endswith(value, arg):
    """Checks if the given value ends with the specified argument."""
    return str(value).endswith(arg)


@register.filter
def is_image(file_url):
    """Checks if the file URL ends with a common image extension."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
    if isinstance(file_url, str):
        return any(file_url.lower().endswith(ext) for ext in image_extensions)
    return False

@register.filter
def contains(value, arg):
    return arg in value if value else False
    
@register.filter
def replace_substring(value, args):
    """Replaces a substring in a string with another substring."""
    try:
        old, new = args.split(',')
        return value.replace(old, new)
    except ValueError:
        return value  # return the original value if the arguments are not correct