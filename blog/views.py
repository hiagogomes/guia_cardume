from django.shortcuts import render, get_object_or_404  # funções úteis: renderiza templates e busca objetos
from .models import Post, Categoria  # importa o modelo Post
from .forms import ComentarioForm, ContatoForm
from django.db.models import Count
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

def home(request):
    posts = Post.objects.order_by('-criado_em')[:3]
    categorias = Categoria.objects.annotate(posts_count=Count('posts')).order_by('nome')
    context = {
        'posts': posts,
        'categorias': categorias,
    }
    return render(request, 'blog/home.html', context)


def sobre(request):
    return render(request, 'blog/sobre.html')

def lista_posts(request):
    categoria_id = request.GET.get('categoria')
    posts = Post.objects.all().order_by('-criado_em')

    if categoria_id:
        posts = posts.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.annotate(num_posts=Count('posts'))

    return render(request, 'blog/lista_posts.html', {
        'posts': posts,
        'categorias': categorias,
        'categoria_id': categoria_id,
    })

def detalhe_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comentarios = post.comentarios.filter(aprovado=True)

    novo_comentario = None

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.post = post
            novo_comentario.save()
    else:
        form = ComentarioForm()

    return render(request, 'blog/detalhe_post.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'novo_comentario': novo_comentario
    })

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'blog/contato.html', {
                'form': ContatoForm(),
                'mensagem_sucesso': 'Mensagem enviada com sucesso!'
            })
    else:
        form = ContatoForm()
    return render(request, 'blog/contato.html', {'form': form})

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /static/",
        "Disallow: /media/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def politica_privacidade(request):
    return render(request, 'blog/politica_privacidade.html')

def termos_uso(request):
    return render(request, 'blog/termos_uso.html')

@require_POST
def aceitar_cookies(request):
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('cookie_consent', 'true', max_age=60*60*24*365)  # 1 ano
    return response

