from django.urls import path
from . import views
from comments.views import CommentListView # Importa la vista

posts_patterns =([
    path("", views.PostListView.as_view(), name="posts_list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("categoria/<str:category_name>/", views.CategoryPostsView.as_view(), name="category_posts"),
    path("fecha/<int:year>/<int:month>/<int:day>/", views.PostByDateView.as_view(), name="posts_by_date"),
    path("autor/<str:username>/", views.AuthorPostsView.as_view(), name="author_posts"),
    path('post/<slug:slug>/comments/', CommentListView.as_view(), name='comment_list'),
    path("categorias/", views.CategoryListView.as_view(), name="category_list"),

],'posts')