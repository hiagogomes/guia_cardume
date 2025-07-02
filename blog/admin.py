from django.contrib import admin
from .models import Post, Comentario, Categoria, MensagemContato, Autor
from django.utils.html import format_html

@admin.register(Post) # registra o modelo com o painel admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'criado_em')
    prepopulated_fields = {'slug': ('titulo',)}  # preenche automaticamente o slug com base no título

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="height: 50px;">', obj.imagem.url)
        return "-"
    imagem_preview.short_description = 'Imagem'

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'post', 'criado_em', 'aprovado')
    list_filter = ('aprovado', 'criado_em')
    search_fields = ('nome', 'email', 'corpo')

@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_envio')
    list_filter = ('data_envio',)
    search_fields = ('nome', 'email', 'mensagem')


admin.site.register(Autor)
admin.site.register(Categoria)
