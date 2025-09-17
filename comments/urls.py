# comments/urls.py

from django.urls import path
from .views import CommentPostView, CommentDeleteView, CommentEditView

comments_patterns = ([
    path('add-comment/<int:pk>/', CommentPostView.as_view(), name='add_comment'),
    path('delete-comment/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),
    path('edit-comment/<int:pk>/', CommentEditView.as_view(), name='edit_comment'),
], 'comments')