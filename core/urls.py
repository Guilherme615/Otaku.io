from django.urls import path
from .views import IndexView
from django.urls import path, include


urlpatterns = [
path('', IndexView.as_view(), name='inicio'),
]
