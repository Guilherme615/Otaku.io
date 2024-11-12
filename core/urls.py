from django.urls import path
from .views import IndexView
from django.urls import path, include
from . import views

urlpatterns = [
path('', IndexView.as_view(), name='inicio'),
path('register/', views.register, name='register'),
]
