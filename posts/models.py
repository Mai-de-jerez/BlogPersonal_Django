from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['-created']

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, always_update=True)
    content = CKEditor5Field(verbose_name='Contenido', blank=True, null=True)
    published = models.DateTimeField(verbose_name='Fecha de publicación', default=now)
    video_embed_url = models.URLField(blank=True, null=True, verbose_name='Video URL')
    url_externa = models.URLField(blank=True, null=True, verbose_name='URL Externa')

    POST_MEDIA_CHOICES = (
        ('none', 'Ninguno'),      
        ('single_image', 'Una sola imagen'),
        ('gallery', 'Galería (Carrusel)'),
        ('video', 'Video'),
    )
    media_type = models.CharField(
        max_length=20,
        choices=POST_MEDIA_CHOICES,
        default='none', 
        verbose_name='Tipo de Contenido Multimedia'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    categories = models.ManyToManyField(Category, verbose_name='Categorías')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    @property
    def has_gallery_images(self):
        return self.gallery_images.exists() 
    
class PostGalleryImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='gallery_images', verbose_name='Post')
    image = models.ImageField(upload_to='post_galleries/', verbose_name='Imagen de Galería')
    caption = models.CharField(max_length=255, blank=True, verbose_name='Título de Imagen')
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')

    class Meta:
        verbose_name = 'Imagen de Galería'
        verbose_name_plural = 'Imágenes de Galería'
        ordering = ['order'] 

    def __str__(self):
        return f"Imagen para '{self.post.title}' (Orden: {self.order})"
    

