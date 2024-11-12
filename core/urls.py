from django.urls import path
from .views import IndexView
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
path('', IndexView.as_view(), name='inicio'),
path('register/', views.register, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('profile_photo/', views.upload_profile_picture, name='profile_photo'),
path('profile/', views.profile_view, name='profile'),  # Nome da URL é 'profile'
path('profile_photo/', views.upload_profile_picture, name='profile_photo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
