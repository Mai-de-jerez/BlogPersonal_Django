# posts/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.timezone import now 
from django.shortcuts import redirect
from .models import Post, PostGalleryImage, Category
from comments.forms import CommentForm, ReplyForm

    
class PostListView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.filter(published__lte=now()).order_by('-published')
        query = self.request.GET.get("s")
        filter_type = self.request.GET.get("filter")

        if query:
            if filter_type == "title":
                queryset = queryset.filter(title__icontains=query)
            elif filter_type == "author":
                queryset = queryset.filter(author__username__icontains=query)
            elif filter_type == "category":
                queryset = queryset.filter(categories__name__icontains=query)

        return queryset
    
class AuthorPostsView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # Obtiene al autor de la URL y si no existe, devuelve un error 404
        self.author = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        
        # Filtra los posts por el autor y asegura que solo se muestren los publicados
        return Post.objects.filter(author=self.author, published__lte=now()).order_by('-published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasa el nombre del autor a la plantilla para que se pueda mostrar el título
        context['title'] = f"Posts de {self.author.get_full_name() or self.author.username}"
        return context

class PostByDateView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        
        # Filtramos por año, mes y día, ignorando la hora del campo `published`.
        return Post.objects.filter(
            published__year=year,
            published__month=month,
            published__day=day,
            published__lte=now()  # Aseguramos que solo se muestren posts publicados
        ).order_by('-published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Posts del {self.kwargs['day']}/{self.kwargs['month']}/{self.kwargs['year']}"
        return context
    
        

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object() 
        context['form'] = CommentForm() 

        # Formulario para responder a comentarios existentes
        if self.request.user.is_authenticated:
            context['reply_form'] = ReplyForm()
        else:
            context['reply_form'] = None

        context['is_post_detail'] = True

        # Incluir solo los comentarios de primer nivel en el contexto
        context['comments'] = post.comments.filter(parent__isnull=True).order_by('-created')[:4]

        # Lógica para posts anteriores y siguientes
        context['prev_post'] = Post.objects.filter(published__lt=post.published).order_by('-published').first()
        context['next_post'] = Post.objects.filter(published__gt=post.published).order_by('published').first()

        # Lógica para posts relacionados
        related_posts = Post.objects.filter(
            categories__in=post.categories.all()
        ).exclude(pk=post.pk).distinct().order_by('-published')[:3]

        if len(related_posts) < 3:
            found_ids = list(related_posts.values_list('pk', flat=True))
            remaining_needed = 3 - len(related_posts)
            
            author_posts = Post.objects.filter(
                author=post.author
            ).exclude(
                pk__in=found_ids + [post.pk]
            ).order_by('-published')[:remaining_needed]

            related_posts = list(related_posts) + list(author_posts)

        context['related_posts'] = related_posts
        
        return context


class CategoryPostsView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return Post.objects.filter(
            categories=self.category, 
            published__lte=now()
        ).order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Posts en {self.category.name}'
        return context
    
class CategoryListView(ListView):
    model = Category
    template_name = 'posts/category_list.html'
    context_object_name = 'categories'

# === Vistas con permisos ===

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'published', 'video_embed_url', 'url_externa', 'media_type', 'categories']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:posts_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'published', 'video_embed_url', 'url_externa', 'media_type', 'categories']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:posts_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:posts_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

   
    
