from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from forms import UserCreateForm
from forms import EventCreateForm
from sponsorsManager.models import UserProfile
# Create your views here.


def main_controller(request, petition):
    if petition == 'home' or petition == 'login':
        return index(request)
    if petition == 'logout':
        return logout_view(request)
    if petition == 'events':
        return event_view(request)
    if request.user.is_authenticated():
        return profile(request, petition)


def login(request):
    if request.user.is_anonymous:
        c = {}
        c.update(csrf(request))
        return render(request, 'sponsorsManager/login.html', c)
    if request.user.is_authenticated:
        return render(request, 'sponsorsManager/index.html',
                      {'full_name': request.user.username})


def auth_view(request):
    # empty string to send as default if empty
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect("/"+request.user.username)
    else:
        return render(request, 'sponsorsManager/invalid.html')


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/"+request.user.username)
        ## toDo: home page. Right now it is redirecting to profile page
    else:
        return login(request)

def profile(request, username):
    return render(request, 'sponsorsManager/profile.html')

def invalid(request):
    return render(request, 'sponsorsManager/invalid.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def event_view(request):
    return render(request, 'sponsorsManager/events.html')

def general_create(request, generic_form, template_name):
    form = generic_form()
    if request.method == 'POST':
        form = generic_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/home")
        else:
            return render(request, template_name, {'form': form, })
    print("holi")
    return render(request, template_name, {'form': form, })


def general_groot(request, instance_id, generic_form, generic_model):
    template_name = "sponsorsManager/forms.html"
    model_instance = generic_model.objects.get(id=instance_id)
    form = generic_form(instance=model_instance)
    if request.method == 'POST':
        form = generic_form(request.POST, instance=model_instance)
        if 'delete' in request.POST:
            model_instance.delete()
            return HttpResponseRedirect("/home")
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/home")
        else:
            return render(request, template_name, {'form': form, })
    print("holi")
    return render(request, template_name, {'form': form, })


