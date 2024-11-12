from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário automaticamente após o registro
            return redirect('home')  # Redireciona para a página inicial
    else:
        form = RegisterForm()
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