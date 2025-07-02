from django import template
from blog.models import Categoria
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('blog/partials/categorias_sidebar.html')
def mostrar_categorias():
    categorias = Categoria.objects.annotate(total=Count('post')).filter(total__gt=0)
    return {'categorias': categorias}
