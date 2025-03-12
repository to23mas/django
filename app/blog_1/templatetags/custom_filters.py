from django import template

register = template.Library()

@register.filter
def can_edit_blog(user):

    return user.groups.filter(name='blog-admin').exists()


