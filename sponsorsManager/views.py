from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse

# Create your views here.
def login(request):
	c = {}
	c.update(csrf(request))
	return render(request, 'sponsorsManager/login.html', c)

def auth_view(request):
	username = request.POST.get('username', '') ##empty string to send as default if empty
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return render(request, 'sponsorsManager/index.html')
	else:
		return render(request, 'sponsorsManager/invalid.html')

def index(request):
	return render(request, 'sponsorsManager/index.html', {'full_name':request.user.username})

def invalid(request):
	return render(request, 'sponsorsManager/invalid.html')