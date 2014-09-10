from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
from forms import UserCreateForm
from sponsorsManager.models import UserProfile
# Create your views here.


def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'sponsorsManager/login.html', c)


def auth_view(request):
    # empty string to send as default if empty
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return render(request, 'sponsorsManager/index.html',
                  {'full_name': request.POST.get('username', '')})
    else:
        return render(request, 'sponsorsManager/invalid.html')


def index(request):
    return render(request, 'sponsorsManager/index.html',
                  {'full_name': request.POST.get('username', '')})


def invalid(request):
    return render(request, 'sponsorsManager/invalid.html')


def signupForm(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            user_data = UserProfile()
            user_data.user = user_instance
            user_data.organization = request.POST.get('organization', '')
            user_data.save()
            print(form.fields)
            return render(request, 'sponsorsManager/index.html',
                          {'full_name': request.POST.get('username', '')})
    else:
        form = UserCreateForm()
    return render(request, 'sponsorsManager/signup.html', {'form': form, })
