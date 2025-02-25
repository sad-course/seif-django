from django import template

register = template.Library()


@register.filter
def is_admin(user):
    return user.groups.filter(name="Administrators").exists()
