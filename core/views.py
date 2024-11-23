from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, ProfilePictureForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        # Verificar se o formulário é válido
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Verificar se o nome de usuário já está em uso
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Esse nome de usuário já está em uso.')
            
            # Verificar se o email já está em uso
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Esse e-mail já está em uso.')
            
            # Se houver erros, retornar ao formulário
            if form.errors:
                return render(request, 'register.html', {'form': form})
            
            # Caso contrário, salvar o usuário
            user = form.save()
            login(request, user)  # Loga o usuário automaticamente após o registro
            return redirect('profile_photo')  # Redireciona para a página de upload de foto de perfil

    else:
        form = CustomUserCreationForm()  # Criar um novo formulário vazio

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo, {user.username}!")
                return redirect('inicio')  # Substitua 'home' pela URL de destino após o login
            else:
                messages.error(request, "Erro ao fazer login. Verifique suas credenciais.")
        else:
            messages.error(request, "Erro ao tentar fazer login. Verifique seus dados.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def upload_profile_picture(request):
    # Obtém ou cria o perfil do usuário autenticado
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Salva a foto no banco de dados
            return redirect('profile')  # Redireciona para a página do perfil
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'profile_photo.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Atualizar ou criar o perfil
    if created:
        Profile.objects.create(user=instance, email=instance.email)
    else:
        profile = Profile.objects.filter(user=instance).first()
        if profile:
            profile.email = instance.email  # Atualiza o email no perfil
            profile.save()

def profile(request):
    user_profile = request.user.profile
    if not user_profile.photo:
        user_profile.photo = 'profile_photos/default_profile.png'
    return render(request, 'profile.html', {'user': request.user})