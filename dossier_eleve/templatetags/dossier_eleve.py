from django import template
from dossier_eleve.views import compute_unread_rows

register = template.Library()


@register.simple_tag
def new_cas():
    return compute_unread_rows()
