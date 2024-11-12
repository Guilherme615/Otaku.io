from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import RegisterForm

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