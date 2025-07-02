from django.urls import path  # importa a função para definir rotas
from . import views  # importa as views

urlpatterns = [
    path('', views.home, name='home'),
    path('lista_posts', views.lista_posts, name='lista_posts'),  # rota da página principal: lista todos os posts
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('politica_privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('termos_uso/', views.termos_uso, name='termos_uso'),
    path('aceitar_cookies/', views.aceitar_cookies, name='aceitar_cookies'),
    path('<slug:slug>/', views.detalhe_post, name='detalhe_post'),  # rota dinâmica para cada post
    
]
