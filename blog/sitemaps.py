from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post  # supondo que seu modelo de posts seja Post

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'lista_posts', 'sobre', 'contato']

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Post.objects.filter(publicado=True)  # ajuste conforme seu modelo

    def lastmod(self, obj):
        return obj.atualizado_em if hasattr(obj, 'atualizado_em') else obj.criado_em
