from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)  
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # Campo de foto de perfil

    def __str__(self):
        return f'{self.name} ({self.email})'

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Remova unique=True caso esteja presente e não seja necessário
    email = models.EmailField(blank=True, null=True)

