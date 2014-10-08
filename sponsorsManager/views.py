from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from forms import UserCreateForm
from forms import UserForm
from forms import EventCreateForm, NeedsCreateForm
from forms import UserEditForm
from forms import UserProfileEditForm
from sponsorsManager.models import UserProfile, Event
# Create your views here.


def main_controller(request, petition):
    if petition == 'home' or petition == 'login':
        return index(request)
    if petition == 'logout':
        return logout_view(request)
    if petition == '404':
        return render(request, 'sponsorsManager/404.html')
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
        profile = UserProfile.objects.get(user=user)
        if profile.is_active():
            auth.login(request, user)
            return HttpResponseRedirect("/" + request.user.username)
        else:
            logout(request)
            return render(request,
                          'sponsorsManager/login.html',
                          {'error_message': 'Invalid login. Try again'},)

    else:
        return render(request,
                      'sponsorsManager/login.html',
                      {'error_message': 'Invalid login. Try again'},)


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
            return HttpResponseRedirect('/' + request.POST['username'])

        else:
            username = request.POST['username']
            user = User.objects.get(username=username)
            print(user)
            if user is not None:
                return render(request,
                              template_name,
                              {'forms': forms,
                               'error_message':
                               'User exists but is deactivated.'})
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


def profile(request, user_name):
    user2 = request.user
    try:
        user = User.objects.get(username=user_name)
        if user == user2 or user is None:
            return render(request, 'sponsorsManager/profile.html')
        else:
            return HttpResponseRedirect('/404')
    except User.DoesNotExist:
        return HttpResponseRedirect('/404')


def invalid(request):
    return render(request, 'sponsorsManager/invalid.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def event_view(request, user_name):
    user2 = request.user
    try:
        user = User.objects.get(username=user_name)
        if user == user2 or user is None:
            return render(request, 'sponsorsManager/my_events.html')
        else:
            return HttpResponseRedirect('/404')
    except User.DoesNotExist:
        return HttpResponseRedirect('/404')

def needs_view(request, user_name, event_name):
    user2 = request.user
    try:
        user = User.objects.get(username=user_name)
        if user == user2 or user is None:
            print(user)
            event = Event.objects.get(name=event_name)
            return render(request, 'sponsorsManager/needs.html',
                {'event': event,
                })
        else:
            return HttpResponseRedirect('/404')
    except User.DoesNotExist:
        return HttpResponseRedirect('/404')


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
            return HttpResponseRedirect('/'+user.username+'/events')
            #return render(request,
             #             template_name,
              #            {'forms': forms,
               #            'success_message': 'Successfully added'})

        else:
            # return form with errors
            forms = [form]
            return render(request,
                          template_name,
                          {'forms': forms, })
    forms = [form]
    return render(request, template_name, {'forms': forms, })

def create_needs(request, user_name, event_name, generic_form, template_name):
    form = generic_form()
    event_instance = Event.objects.get(name=event_name)
    if request.method == 'POST':
        form = generic_form(request.POST)
        if form.is_valid():
            user = request.user
            if user.is_authenticated():
                data = user.user_data
                instance = form.save(commit=False)
                instance.event = event_instance
            form.save()
            forms = [form]
            return HttpResponseRedirect('/'+user.username+'/events/')
            #return render(request,
             #             template_name,
              #            {'forms': forms,
               #            'success_message': 'Successfully added'})

        else:
            # return form with errors
            forms = [form]
            return render(request,
                          template_name,
                          {'forms': forms, })
    forms = [form]
    return render(request, template_name, {'forms': forms, })



def groot_user(request, user_name):
    if(request.user.is_authenticated()):
        user2 = request.user
        try:
            user = User.objects.get(username=user_name)
            if user == user2 or user is None:
                uform = UserEditForm()
                pform = UserProfileEditForm()
                template_name = 'sponsorsManager/user_edit.html'
                model_profile_instance = UserProfile.objects.get(
                    user=request.user)
                pform = UserProfileEditForm(instance=model_profile_instance)
                model_user_instance = request.user
                uform = UserEditForm(
                    initial={'username': request.user},
                    instance=model_user_instance)
                forms = [uform, pform]
                if request.method == "POST":
                    uform = UserEditForm(request.POST,
                                         initial={'username': request.user},
                                         instance=model_user_instance)
                    pform = UserProfileEditForm(
                        request.POST, instance=model_profile_instance)
                    print(request.POST)
                    if 'deactivate' in request.POST:
                        if request.user.check_password(
                                request.POST.get('password', '')):
                            print("yep, let's erase this.")
                            user = uform.save()
                            password = request.POST.get('password', '')
                            user.set_password(password)
                            user.save()
                            profile = pform.save(commit=False)
                            profile.active = 0
                            profile.user = user
                            profile.save()
                            logout(request)
                            return HttpResponseRedirect('/home')

                        else:
                            forms = [uform, pform]
                            return render(request,
                                          template_name, {'forms': forms,
                                                          'success_message':
                                                          'Incorrect' +
                                                          ' password' +
                                                          '. Try again'})
                    elif uform.is_valid() and pform.is_valid():
                        user = uform.save()
                        password = request.POST.get('password', '')
                        user.set_password(password)
                        user.save()
                        profile = pform.save(commit=False)
                        profile.user = user
                        profile.save()
                        user = authenticate(username=request.user,
                                            password=password)
                        login(request, user)
                        return HttpResponseRedirect('/home')
                    else:
                        # return form with errors
                        forms = [uform, pform]
                        return render(request, template_name, {'forms': forms})
                forms = [uform, pform]
                return render(request, template_name, {'forms': forms, })
            else:
                return HttpResponseRedirect('/404')
        except User.DoesNotExist:
            return HttpResponseRedirect('/404')

    else:
        return index(request)


def general_groot(request,
                  user_name,
                  instance_id,
                  generic_form,
                  template_name,
                  generic_model):
    model_instance = generic_model.objects.get(name=instance_id)
    form = generic_form(instance=model_instance)
    if request.method == 'POST':
        form = generic_form(request.POST, instance=model_instance)
        if 'delete' in request.POST:
            model_instance.delete()
            return HttpResponseRedirect("/"+user_name+"/events")
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/"+user_name+"/events")
        else:
            forms = [form]
            return render(request, template_name, {'forms': forms, 'event': instance_id})
    else:
        print("holi")
        forms = [form]
        return render(request, template_name, {'forms': forms, 'event': instance_id})

def groot_needs(request,
                  user_name,
                  event_name,
                  instance_id,
                  generic_form,
                  template_name,
                  generic_model):
    model_instance = generic_model.objects.get(name=instance_id)
    form = generic_form(instance=model_instance)
    if request.method == 'POST':
        form = generic_form(request.POST, instance=model_instance)
        if 'delete' in request.POST:
            model_instance.delete()
            return HttpResponseRedirect("/"+user_name+"/events")
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/"+user_name+"/events")
        else:
            forms = [form]
            return render(request, template_name, {'forms': forms, 'event': instance_id})
    else:
        print("holi")
        forms = [form]
        return render(request, template_name, {'forms': forms, 'event': instance_id})


def history (request, user_name):
    return HttpResponseRedirect('/404')