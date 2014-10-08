from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from forms import UserCreateForm
from forms import UserForm
from forms import EventCreateForm
from forms import UserEditForm
from forms import UserProfileEditForm
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


def my_login(request):
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
    print(username)
    password = request.POST.get('password', '')
    print(password)
    user = auth.authenticate(username=username, password=password)
    print(user)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect("/" + request.user.username)
    else:
        return render(request,
                      'sponsorsManager/login.html',
                      {'error_message': 'Invalid login. Try again'},
                      )


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/" + request.user.username)
        # toDo: home page. Right now it is redirecting to profile page
    else:
        return my_login(request)


def signup(request):
    uform = UserForm()
    pform = UserCreateForm()
    forms = [uform, pform]
    for form in forms:
        print(form)

    template_name = 'sponsorsManager/signup.html'
    if request.method == "POST":
        uform = UserForm(request.POST)
        pform = UserCreateForm(request.POST)
        forms = [uform, pform]

        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            password = request.POST.get('password', '')
            print(password)
            user.set_password(password)
            user.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
            template_name = 'sponsorsManager/profile.html'
            user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, user)
            forms = {uform, pform}
            return HttpResponseRedirect("/home")
        else:
            # return form with errors
            return render(request, template_name, {'forms': forms, })
    return render(request, template_name, {'forms': forms})


def home_with_message(request, message):
    if request.user.is_authenticated():
        HttpResponseRedirect("/home")
        return render(request, 'sponsorsManager/home.html')
        # toDo: home page. Right now it is redirecting to profile page
    else:
        return my_login(request)


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
            user = request.user
            if user.is_authenticated():
                data = user.user_data
                instance = form.save(commit=False)
                instance.user = user
            form.save()
            forms = [form]
            return render(request,
                          template_name,
                          {'forms': forms,
                           'success_message': 'Successfully added'})

        else:
            # return form with errors
            forms = [form]
            return render(request,
                          template_name,
                          {'forms': forms, })
    forms = [form]
    return render(request, template_name, {'forms': forms, })


def groot_user(request, user_name):
    print(request.user.is_authenticated())
    if(request.user.is_authenticated()):
        uform = UserEditForm()
        pform = UserProfileEditForm()
        template_name = 'sponsorsManager/user_edit.html'
        model_profile_instance = UserProfile.objects.get(user=request.user)
        pform = UserProfileEditForm(instance=model_profile_instance)
        model_user_instance = request.user
        uform = UserEditForm(
            initial={'username': request.user}, instance=model_user_instance)
        forms = [uform, pform]
        if request.method == "POST":
            print(request.user)
            uform = UserEditForm(request.POST,
                                 initial={'username': request.user},
                                 instance=model_user_instance)
            pform = UserProfileEditForm(
                request.POST, instance=model_profile_instance)
            if 'delete' in request.POST:
                # ToDo: delete. Decide how to do it
                print('do nothing')
            if uform.is_valid() and pform.is_valid():
                user = uform.save()
                password = request.POST.get('password', '')
                user.set_password(password)
                user.save()
                profile = pform.save(commit=False)
                profile.user = user
                profile.save
                user = authenticate(username=request.user,
                                    password=request.POST['password'])
                login(request, user)
                forms = [uform, pform]
                return render(request,
                              template_name,
                              {'forms': forms,
                               'success_message': 'Successfully changed'}
                              )
            else:
                # return form with errors
                forms = [uform, pform]
                return render(request, template_name, {'forms': forms})
        forms = [uform, pform]
        return render(request, template_name, {'forms': forms, })
    else:
        return index(request)


def general_groot(request, instance_id,
                  generic_form, template_name,
                  generic_model):
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
