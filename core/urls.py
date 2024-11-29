from django.urls import path
from .views import IndexView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),  # URL para o perfil
    path('profile_photo/', views.upload_profile_picture, name='profile_photo'),  # Corrigido duplicata
    path('cadastrar-obra/', views.cadastrar_obra, name='cadastrar_obra'),  # Nome correto
    path('listar-obras/', views.listar_obras, name='listar_obras'),
    path('editar-obra/<int:obra_id>/', views.editar_obra, name='editar_obra'),
    path('excluir-obra/<int:obra_id>/', views.excluir_obra, name='excluir_obra'),
    path('obra/<str:titulo>/', views.detalhes_obra, name='detalhes_obra'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
