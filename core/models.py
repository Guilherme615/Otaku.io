from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)  
    email = models.EmailField(unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Remova unique=True caso esteja presente e não seja necessário
    email = models.EmailField(blank=True, null=True)

class Obra(models.Model):
    titulo = models.CharField(max_length=255)
    capa = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Opiniao(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='opinioes')
    usuario = models.CharField(max_length=50)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Opinião de {self.usuario} em {self.obra.titulo}"