from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'updated')
    list_filter = ('created','post')
    search_fields = ('name', 'email', 'text', 'author__username') 
    readonly_fields = ('created', 'updated')
    ordering = ('-created',) 
    list_per_page = 20  

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.order_by('-created')
        return qs.none()
    

