from posts.models import Category, Post
from django.utils.timezone import now

def categories(request):
    """
    Agrega la lista de categorías a todas las plantillas.
    """
    return {
        'categories_list': Category.objects.all()
    }

def latest_posts(request):
    """
    Agrega los 5 posts más recientes a todas las plantillas.
    """
    posts = Post.objects.filter(published__lte=now()).order_by('-published')[:5]
    return {
        'latest_posts_list': posts
    }