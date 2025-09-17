from django.shortcuts import render, redirect
from posts.models import Post 
from django.db.models import Q
from django.views.generic import TemplateView
from django.utils.timezone import now 
from django.core.mail import send_mail  
from django.conf import settings        
from .forms import ContactForm  

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Enviar el correo electrónico
            send_mail(
                f'Mensaje de contacto de {name}',
                f"De: {email}\n\n{message}",
                settings.EMAIL_HOST_USER, # El remitente (el correo que configuraste)
                [settings.EMAIL_HOST_USER], # El destinatario (tu correo)
                fail_silently=False,
            )
            return redirect('contact') # Redirige a la misma página o a una de éxito
    else:
        form = ContactForm()
    
    return render(request, "core/contact.html", {'form': form})

def gallery(request):
    # Recupera posts que tengan AL MENOS UNA imagen en su relación gallery_images
    # y que no sean de tipo 'video' o 'none'.
    all_gallery_posts = Post.objects.filter(
        gallery_images__isnull=False 
    ).exclude(
        media_type='video'
    ).exclude(
        media_type='none'
    ).order_by('-published').distinct() 

    context = {
        'featured_gallery_posts': all_gallery_posts,  
        'title': 'Nuestra Galería de Fotos', 
    }
    return render(request, "core/gallery.html", context)

