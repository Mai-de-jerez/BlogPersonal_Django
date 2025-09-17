# comments/models.py

from django.db import models
from django.conf import settings # Importa la configuración de Django
from django_ckeditor_5.fields import CKEditor5Field
from posts.models import Post # Importa el modelo Post para la relación

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Post')
    # Campos originales que se mantendrán
    name = models.CharField(max_length=80, verbose_name='Nombre')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    text = CKEditor5Field(verbose_name='Comentario')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    # Nuevo campo que se usará para la autenticación y permisos
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments_auth', verbose_name='Autor', null=True)
    # Nuevo campo para el anidamiento (respuestas a comentarios)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return self.name + ' - ' + self.post.title
