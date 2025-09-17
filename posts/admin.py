from django.contrib import admin
from .models import Post, Category, PostGalleryImage


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class PostGalleryImageInline(admin.TabularInline):
    model = PostGalleryImage
    extra = 1
    fields = ('image', 'caption', 'order') 

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    inlines = [PostGalleryImageInline]
    list_display = ('title', 'author', 'created', 'updated', 'published')

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

