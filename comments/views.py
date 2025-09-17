# comments/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from posts.models import Post
from .models import Comment
from .forms import CommentForm, ReplyForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
 
    
        
@method_decorator(login_required, name='dispatch')
class CommentPostView(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        
        # Decide qué formulario usar
        parent_id = request.POST.get('parent_id')
        if parent_id:
            form = ReplyForm(request.POST)  
        else:
            form = CommentForm(request.POST) 

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            
            comment.author = request.user
            comment.name = request.user.username
            comment.email = request.user.email

            if parent_id:
                comment.parent = get_object_or_404(Comment, pk=parent_id)

            comment.save()
            messages.success(request, '¡Tu comentario ha sido añadido con éxito!')

            # Redirigir a la misma página desde donde se envió el comentario
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('posts:post_detail', args=[post.pk])
            return redirect(f"{next_url}#comment-{comment.pk}")
        
        else:
            messages.error(request, 'Ha ocurrido un error al enviar tu comentario.')
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('posts:post_detail', args=[post.pk])
            return redirect(next_url)
    
class CommentListView(ListView):
    model = Comment
    template_name = 'comments/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 5

    
    def get_queryset(self):
        post_slug = self.kwargs['slug']
        parent_id = self.request.GET.get('respuestas')

        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id, post__slug=post_slug)
            self.parent_comment = parent
            return Comment.objects.filter(parent=parent).order_by('created')

        return Comment.objects.filter(post__slug=post_slug, parent__isnull=True).order_by('-created')
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context['post'] = post  

        if hasattr(self, 'parent_comment'):
            context['parent_comment'] = self.parent_comment

        context['reply_form'] = ReplyForm() if self.request.user.is_authenticated else None
        return context

class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    
    def get_success_url(self):
        return reverse_lazy('posts:comment_list', args=[self.object.post.slug]) + f"#comment-{self.object.pk}"
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_superuser
    


class CommentEditView(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_edit.html'
    
    
    def get_success_url(self):
        return reverse_lazy('posts:comment_list', args=[self.object.post.slug]) + f"#comment-{self.object.pk}"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_superuser
 