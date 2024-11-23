from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, label="Nome")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']  # Campo usado para armazenar a foto de perfil

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise ValidationError("Esse email já está em uso.")
        return email