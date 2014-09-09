from django.shortcuts import render
from django.template import RequestContext, loader
# Create your views here.
def login(request):
	hola = 'hola'
	return render(request, 'sponsorsManager/login.html')