from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, ProfilePictureForm, ObraForm, SolicitacaoObraForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile, Obra, Opiniao, SolicitacaoObra
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import random
from django.core.exceptions import PermissionDenied


# Página inicial
class IndexView(View):
    def get(self, request):
        # Pega todas as obras cadastradas
        obras = Obra.objects.all()
        
        # Embaralha as obras e pega as 10 primeiras
        random_obras = random.sample(list(obras), min(len(obras), 10))
        
        return render(request, 'index.html', {'obras': random_obras})

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
        if "texto" in request.POST:
            # Se for uma opinião nova
            usuario = request.user
            texto = request.POST.get("texto")
            if usuario and texto:
                Opiniao.objects.create(obra=obra, usuario=usuario.username, texto=texto)

        elif "delete_opiniao_id" in request.POST:
            # Se for para excluir uma opinião
            opiniao_id = request.POST.get("delete_opiniao_id")
            opiniao = Opiniao.objects.filter(id=opiniao_id, usuario=request.user.username).first()
            if opiniao:
                opiniao.delete()
            # Depois de excluir, redirecionar para a página de detalhes da obra
            return redirect('detalhes_obra', titulo=obra.titulo)

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
    obras_list = Obra.objects.all()
    paginator = Paginator(obras_list, 5)  # Show 10 obras per page.
    
    page_number = request.GET.get('page')
    obras = paginator.get_page(page_number)

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

@login_required
def solicitar_obra(request):
    if request.method == 'POST':
        form = SolicitacaoObraForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()
            return redirect('minhas_solicitacoes')
    else:
        form = SolicitacaoObraForm()
    return render(request, 'solicitar_obra.html', {'form': form})


@login_required
def minhas_solicitacoes(request):
    solicitacoes = SolicitacaoObra.objects.filter(usuario=request.user)
    return render(request, 'minhas_solicitacoes.html', {'solicitacoes': solicitacoes})


@login_required# Apenas administradores
def gerenciar_solicitacoes(request):
    solicitacoes = SolicitacaoObra.objects.all()
    return render(request, 'gerenciar_solicitacoes.html', {'solicitacoes': solicitacoes})


@login_required # Apenas administradores
def confirmar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoObra, id=solicitacao_id)
    solicitacao.status = 'aprovado'
    solicitacao.save()
    return redirect('gerenciar_solicitacoes')

def rejeitar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoObra, id=solicitacao_id)
    solicitacao.status = 'rejeitado'
    solicitacao.save()
    return redirect('gerenciar_solicitacoes')

@login_required
def limpar_solicitacoes(request):
    # Verifica se o usuário é administrador
    if not request.user.is_superuser:
        raise PermissionDenied
    
    # Limpa todas as solicitações
    SolicitacaoObra.objects.all().delete()

    # Redireciona de volta para a página de gerenciamento de solicitações
    return redirect('gerenciar_solicitacoes')

@login_required
def excluir_solicitacao(request, id):
    # Verifica se o usuário é o proprietário da solicitação ou administrador
    solicitacao = get_object_or_404(SolicitacaoObra, id=id, usuario=request.user)

    # Exclui a solicitação
    solicitacao.delete()

    # Redireciona de volta para a página de Minhas Solicitações
    return redirect('minhas_solicitacoes')

@login_required
def editar_opiniao(request, id):
    opiniao = get_object_or_404(Opiniao, id=id, usuario=request.user)
    if request.method == "POST":
        novo_texto = request.POST.get("texto", "").strip()
        if novo_texto:
            opiniao.texto = novo_texto
            opiniao.save()
            return redirect('detalhes_obra', titulo=opiniao.obra.titulo)
    return render(request, 'editar_opiniao.html', {'opiniao': opiniao})

@login_required
def excluir_opiniao(request, id):
    opiniao = get_object_or_404(Opiniao, id=id, usuario=request.user)
    if request.method == "POST":
        opiniao.delete()
        return redirect('detalhes_obra', titulo=opiniao.obra.titulo)
    return render(request, 'excluir_opiniao.html', {'opiniao': opiniao})

def todas_as_obras(request):
    obras_list = Obra.objects.all()
    paginator = Paginator(obras_list, 8)  # 8 obras por página

    page = request.GET.get('page')
    obras = paginator.get_page(page)

    return render(request, 'todas_as_obras.html', {'obras': obras})