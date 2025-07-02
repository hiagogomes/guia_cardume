from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='autores/')
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) # campo usado na URL (sem espaços e co hífens), deve ser único
    # autor = models.CharField(max_length=100)
    conteudo = CKEditor5Field('Texto do post', config_name='default')
    criado_em = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, related_name='posts')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    publicado = models.BooleanField(default=True)

    imagem = models.ImageField(upload_to='posts/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('detalhe_post', kwargs={'slug': self.slug})
    
    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'image': 'get_meta_image',
        'url': 'get_absolute_url',
    }

    def get_meta_title(self):
        return self.titulo

    def get_meta_description(self):
        return self.conteudo[:150]

    def get_meta_image(self):
        if self.imagem:
            return self.imagem.url
        return None


class Meta:
    ordering = ['-criado_em'] # os posts serão ordenados do mais novo para o mais antigo

    def __str__(self): # método especial para exibir o post de forma legivel
        return self.titulo # retorna o título como representação do post

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    nome = models.CharField(max_length=80)
    email = models.EmailField()
    corpo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Comentário de {self.nome} em {self.post}'


class MensagemContato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f'{self.nome} - {self.email}'
    