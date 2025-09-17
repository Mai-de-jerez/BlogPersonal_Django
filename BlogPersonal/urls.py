"""
URL configuration for BlogPersonal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from posts.urls import posts_patterns
from comments.urls import comments_patterns

urlpatterns = [
    # paths del core
    path("", include("core.urls")),
    # paths del blog
    path("posts/", include(posts_patterns)),
    # paths del admin
    path("admin/", admin.site.urls),
    path("comments/", include(comments_patterns)),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
