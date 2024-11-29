from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)  
    email = models.EmailField(unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Obra(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    capa = models.ImageField(upload_to='capas/', null=True, blank=True)  # Configura o diretório para uploads

    def __str__(self):
        return self.titulo

class Opiniao(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='opinioes')
    usuario = models.CharField(max_length=50)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opinião de {self.usuario} em {self.obra.titulo}"

class SolicitacaoObra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitacoes")
    titulo = models.CharField(max_length=200)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('Pendente', 'Pendente'),
            ('Aprovada', 'Aprovada'),
            ('Recusada', 'Recusada')
        ),
        default='Pendente'
    )

    def __str__(self):
        return f"Solicitação de {self.usuario.username} - {self.titulo}"