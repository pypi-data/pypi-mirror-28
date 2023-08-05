from django import template

register = template.Library()

@register.filter(name="mine")
def do_mine(val):
    return 'modified by customized filter: %s' % val
