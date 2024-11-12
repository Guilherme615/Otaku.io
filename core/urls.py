from django.urls import path
from .views import IndexView
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
path('', IndexView.as_view(), name='inicio'),
path('register/', views.register, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
