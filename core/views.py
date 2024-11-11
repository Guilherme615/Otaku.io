from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
