from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, ProfilePictureForm, ObraForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile, Obra, Opiniao
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import random

# Página inicial
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# Registro de usuário
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Verificar se o nome de usuário e o e-mail já estão em uso
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Esse nome de usuário já está em uso.')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Esse e-mail já está em uso.')
            
            if form.errors:
                return render(request, 'register.html', {'form': form})
            
            user = form.save()
            login(request, user)  # Loga o usuário automaticamente após o registro
            return redirect('profile_photo')  # Redireciona para a página de upload de foto de perfil

    else:
        form = CustomUserCreationForm()  # Criar um novo formulário vazio

    return render(request, 'register.html', {'form': form})

# Login de usuário
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
                return redirect('inicio')
            else:
                messages.error(request, "Erro ao fazer login. Verifique suas credenciais.")
        else:
            messages.error(request, "Erro ao tentar fazer login. Verifique seus dados.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Upload de foto de perfil
@login_required
def upload_profile_picture(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Salva a foto no banco de dados
            return redirect('profile')  # Redireciona para a página do perfil
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'profile_photo.html', {'form': form})

# Exibe o perfil do usuário
@login_required
def profile_view(request):
    return render(request, 'profile.html')

# Criação e atualização automática do perfil de usuário
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)
    else:
        profile = Profile.objects.filter(user=instance).first()
        if profile:
            profile.email = instance.email
            profile.save()

# Página de perfil
def profile(request):
    user_profile = request.user.profile
    if not user_profile.photo:
        user_profile.photo = 'profile_photos/default_profile.png'
    return render(request, 'profile.html', {'user': request.user})

# Detalhes da obra
def detalhes_obra(request, titulo):
    obra = Obra.objects.filter(titulo=titulo).first()

    if not obra:
        obra = Obra.objects.create(titulo=titulo, capa=f"{titulo}.jpg")

    opinioes = Opiniao.objects.filter(obra=obra).order_by('-data_criacao')

    if request.method == "POST":
        usuario = request.user.username
        texto = request.POST.get("texto")
        if usuario and texto:
            Opiniao.objects.create(obra=obra, usuario=usuario, texto=texto)

    return render(request, 'opiniao.html', {'obra': obra, 'opinioes': opinioes})

# Cadastro de obra
def cadastrar_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redireciona para a página inicial
    else:
        form = ObraForm()
    return render(request, 'cadastrar_obra.html', {'form': form})

# Listagem de obras
def listar_obras(request):
    obras = list(Obra.objects.all())
    random.shuffle(obras)  # Embaralha as obras
    return render(request, 'listar_obras.html', {'obras': obras})


# Edição de obra
def editar_obra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES, instance=obra)
        if form.is_valid():
            form.save()
            return redirect('listar_obras')
    else:
        form = ObraForm(instance=obra)
    return render(request, 'editar_obra.html', {'form': form})

# Exclusão de obra
def excluir_obra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    if request.method == 'POST':
        obra.delete()
        return redirect('listar_obras')
    return render(request, 'confirmar_exclusao.html', {'obra': obra})

# Página inicial com obras para o slider
def index(request):
    # Obtém todas as obras cadastradas
    obras = Obra.objects.all()
    
    # Seleciona até 10 obras aleatórias, sem repetir
    obras_slider = random.sample(list(obras), min(len(obras), 10))
    
    # Retorna a renderização da página com as obras e suas respectivas capas
    return render(request, 'index.html', {'obras_slider': obras_slider})

