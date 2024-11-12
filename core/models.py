from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)  
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

# Create your models here.
