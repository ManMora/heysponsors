# -*- encoding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from forms import UserCreateForm, UserForm, EventCreateForm, EventReadForm
from forms import NeedsCreateForm, UserEditForm, UserProfileEditForm
from forms import SponsorshipCreateForm
from sponsorsManager.models import UserProfile, Event, Benefit, ActivityReport
from sponsorsManager.models import Needs, Sponsors, Sponsorship
from sponsorsManager.models import Concession, LogActivity
import requests
import json
# Create your views here.


def main_controller(request, petition):
    user = request.user
    if petition == 'history':
        return history(request)
    if petition == 'emails':
        return send_emails(request)
    if petition == 'home' or petition == 'login':
        return index(request)
    if petition == 'logout':
        return logout_view(request)
    if petition == 'sponsors':
        return getsponsors(request)
    if petition == 'add_sponsorship':
        return add_sponsorship(request, -1, -1)
    if petition == '404':
        return render(request, 'sponsorsManager/404.html')
    if petition == 'my_events':
        return list_objects(request,
                            'sponsorsManager/my_events.html',
                            user)
    if request.user.is_authenticated():
        return profile(request, petition)
    else:
        HttpResponseRedirect("/404")


def add_to_log(request, text):
    activity_instance = ActivityReport.objects.get_or_create(
        user=request.user,
    )
    activity_instance = ActivityReport.objects.get(
        user=request.user,
    )
    print(activity_instance)
    log_instance = LogActivity.objects.create(
        report=activity_instance,
        content=text
    )
    log_instance.save()


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
            add_to_log(
                request, "User " + user.username + " joined the application"
            )
            messages.add_message(request, messages.SUCCESS,
                                 "Congratulations! Welcome to Hey Sponsors!")
            return HttpResponseRedirect('/' + request.POST['username'])

        else:
            username = request.POST['username']
            user = User.objects.get(username=username)
            print(user)
            if user is not None:
                messages.add_message(request, messages.ERROR,
                                     "User exists but is deactivated.",
                                     extra_tags="danger")
                return render(request,
                              template_name,
                              {'forms': forms, })
            # return form with errors
            messages.add_message(request, messages.ERROR,
                                 "Errors in form",
                                 extra_tags="danger")
            return render(request, template_name, {'forms': forms, })
    messages.add_message(request, messages.INFO, "Fill all the fields")
    return render(request, template_name, {'forms': forms})


def profile(request, user_name):
    user2 = request.user
    try:
        user = User.objects.get(username=user_name)
        if user == user2 or user is None:
            all_events = user.Events.all()
            filtered_events = all_events.order_by(
                'date').filter(
                date__gte=datetime.now(),
                finished=False,
                active=True
            )[:5]
            return render(request, 'sponsorsManager/profile.html',
                          {'events': filtered_events}
                          )
        else:
            return HttpResponseRedirect('/404')
    except User.DoesNotExist:
        return HttpResponseRedirect('/404')


def invalid(request):
    return render(request, 'sponsorsManager/invalid.html')


def logout_view(request):
    add_to_log(request, 'Log out')
    logout(request)
    return HttpResponseRedirect("/")


def list_objects(
        request,
        template_name,
        parent_instance):
    user = request.user
    if user.is_authenticated():
        return render(request, template_name,
                      {'parent': parent_instance})


def list_needs(request, instance_id):
    event = Event.objects.get(id=instance_id)
    return list_objects(
        request,
        'sponsorsManager/needs.html',
        event)


def list_sponsorships(request, instance_id):
    event = Event.objects.get(id=instance_id)

    return list_objects(
        request,
        'sponsorsManager/sponsorships.html',
        event)


def general_create(request, instance_id, generic_model, generic_form,
                   template_name, auxiliar_id):
    form = generic_form()
    if request.method == 'POST':
        form = generic_form(request.POST)
        if form.is_valid():
            user = request.user
            if user.is_authenticated():
                data = user.user_data
                instance = form.save(commit=False)
                if(generic_model == Needs):
                    event_instance = Event.objects.get(id=instance_id)
                    instance.event = event_instance
                elif(generic_model == Event):
                    instance.user = user
                elif(generic_model == Sponsorship):
                    instance = form.save(commit=False)
                    event_instance = Event.objects.get(id=instance_id)
                    instance.event = event_instance
                    print(event_instance.name)
                    sponsor_instance = Sponsors.objects.get(id=auxiliar_id)
                    instance.sponsor = sponsor_instance
                    benefits = request.POST.get('benefits_2', '')
                    benefits_instance = Benefit.objects.create(
                        #name='Benefits with ' + str(sponsor_instance.name),
                        name='Benefits with ' + sponsor_instance.name,
                        description=benefits
                    )
                    instance.benefits = benefits_instance
                    concesions = request.POST.get('concesions_2', '')
                    concesions_instance = Concession.objects.create(
                        name='Concesions with ' + sponsor_instance.name,
                        description=concesions
                    )
                    instance.concesions = concesions_instance
                    sponsor = Sponsorship.objects.create(
                        sponsor=sponsor_instance,
                        event=event_instance,
                        concesions=concesions_instance,
                        benefits=benefits_instance,
                    )

                    return HttpResponseRedirect('/my_events')
            messages.add_message(
                request, messages.SUCCESS, 'Successfully added!')
            form.save()
            forms = [form]
            return HttpResponseRedirect('/my_events')
            return render(request,
                          template_name,
                          {'forms': forms,
                           'success_message': 'Successfully added'})
        else:

            # return form with errors
            forms = [form]
            messages.add_message(request, messages.ERROR, 'Errors',
                                 extra_tags='danger')
            return render(
                request,
                template_name,
                {'forms': forms, }
            )
    forms = [form]
    messages.add_message(request, messages.INFO, 'Fill the fields')

    return render(request, template_name, {'forms': forms, })


def getsponsors(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            if'query' in request.POST:
                events = list(Event.objects.all().filter(user=request.user))
                payload = {
                    'url': 'http://www.seccionamarilla.com.mx/resultados/'
                    + request.POST.get('query') + '/1'}
                print(payload)
                r = requests.post(
                    "http://127.0.0.1:8000/crawler/gettags/", data=payload)
                print(r)
                if r.content != None:
                    return render(request, 'sponsorsManager/getsponsors.html',
                                  {'events': events,
                                   'sponsors': json.loads(r.content)
                                   })
        else:
            events = list(Event.objects.all())
            return render(request, 'sponsorsManager/getsponsors.html',
                          {'events': events})


def my_info(request, user_name):
    if request.user.is_authenticated():
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
                        request.POST, instance=model_profile_instance
                    )
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
                            messages.add_message(request, messages.SUCCESS,
                                                 "Correctly deactivated")

                            return HttpResponseRedirect('/home')

                        else:
                            forms = [uform, pform]
                            messages.add_message(request, messages.ERROR,
                                                 "Incorrect password",
                                                 extra_tags="danger")

                            return render(request,
                                          template_name, {'forms': forms,})
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
                        messages.add_message(request, messages.SUCCESS,
                                             "Correctly uploaded")
                        return HttpResponseRedirect('/home')
                    else:
                        # return form with errors
                        forms = [uform, pform]
                        messages.add_message(request, messages.ERROR,
                                             "Errors in form",
                                             extra_tags="danger")
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
                  instance_id,
                  generic_form,
                  template_name,
                  generic_model):
    model_instance = generic_model.objects.get(id=instance_id)
    form = generic_form(instance=model_instance)
    redirect = "/my_events"
    if request.method == 'POST':
        form = generic_form(request.POST, instance=model_instance)
        if 'cancel' in request.POST:
            model_instance.active = 0
            model_instance.save()
            add_to_log(request, "Canceled " +
                       generic_model._meta.verbose_name.title() +
                       " " +
                       model_instance.name)
            return HttpResponseRedirect(redirect)
        if 'reactivate' in request.POST:
            model_instance.active = True
            model_instance.finished = False
            add_to_log(request, "Reactivated " +
                       generic_model._meta.verbose_name.title() +
                       " " +
                       model_instance.name)
            model_instance.save()
            return HttpResponseRedirect(redirect)
        if 'finish' in request.POST:
            add_to_log(request, "Finished " +
                       generic_model._meta.verbose_name.title() +
                       " " +
                       model_instance.name)
            print(model_instance.finished)
            model_instance.finished = True
            print(model_instance.finished)
            model_instance.save()
            return HttpResponseRedirect(redirect)
        if 'delete' in request.POST:
            add_to_log(request, "Deleted " +
                       generic_model._meta.verbose_name.title() +
                       " " +
                       model_instance.name)
            print model_instance
            messages.add_message(
                request, messages.SUCCESS, 'Successfully deleted!')
            model_instance.delete()
            return HttpResponseRedirect(redirect)
        if form.is_valid():
            add_to_log(request, "Updated " +
                       generic_model._meta.verbose_name.title() +
                       " " +
                       model_instance.name)
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Successfully updated!')
            return HttpResponseRedirect(redirect)
        else:
            forms = [form]
            messages.add_message(request, messages.ERROR, 'Errors in form',
                                 extra_tags='danger')
            # return render(request, template_name,
            #              {'forms': forms, 'parent': model_instance.id})
        if(generic_model == Needs):
            event = Event.objects.get(Needs=model_instance.id)
            redirect = "/needs/" + str(instance_id)
        elif generic_model == Benefit:
            sponsorship = Sponsorship.objects.get(benefits=model_instance)
            event = Event.objects.get(Sponsorships=sponsorship)
            redirect = "/events/" + str(event.id) + "/sponsorships"
        elif generic_model == Concession:
            sponsorship = Sponsorship.objects.get(concesions=model_instance)
            event = Event.objects.get(Sponsorships=sponsorship)
            redirect = "/events/" + str(event.id) + "/sponsorships"
        return HttpResponseRedirect(redirect)
    else:
        forms = [form]
        if generic_model == Event:
            return render(request, template_name,
                          {'forms': forms, 'parent': model_instance.id,
                           'event': Event.objects.get(id=model_instance.id)},)
        if generic_model == Sponsorship:
            ev = Event.objects.get(Sponsorships=model_instance.id)
            spon = Sponsorship.objects.get(id=model_instance.id)
            return render(request, template_name,
                          {'forms': forms, 'parent': model_instance.id,
                           'event': ev, 'sponsorship': spon, },)
        if generic_model == Benefit:
            spon = Sponsorship.objects.get(benefits=model_instance.id)
            ev = Event.objects.get(Sponsorships=spon.id)
            return render(request, template_name,
                          {'forms': forms, 'parent': model_instance.id,
                           'event': ev, 'sponsorship': spon,
                           'title': 'Update benefits'},)
        if generic_model == Concession:
            spon = Sponsorship.objects.get(concesions=model_instance.id)
            ev = Event.objects.get(Sponsorships=spon.id)
            return render(request, template_name,
                          {'forms': forms, 'parent': model_instance.id,
                           'event': ev, 'sponsorship': spon,
                           'title': 'Update Concessions' },)
        if generic_model == Needs:
            ev = Event.objects.get(Needs=model_instance.id)
            return render(request, template_name,
                          {'forms': forms, 'parent': model_instance.id,
                           'event': ev, },)
        else:
            return render(request, template_name,
                          {'forms': forms, 'parent': model_instance.id})


def history(request):
    user = request.user
    if user is None:
        return HttpResponseRedirect('/404')
    else:
        template_name = "sponsorsManager/history.html"
        report = ActivityReport.objects.get(user=user)
        logs = LogActivity.objects.filter(report=report)
        return render(request, template_name, {'logs': logs, }, )


def add_sponsorship(request, event_id, sponsors_id):

    if sponsors_id == -1 and event_id == -1:

        event_id = request.POST.get('dropdown', '')
        if event_id == 'none':
            messages.add_message(
            request, messages.ERROR, 'You didn\'t select an event',
            extra_tags="danger"
            )
            return HttpResponseRedirect('/sponsors')

        print(event_id)
        name = request.POST.get('name', '')
        tel = request.POST.get('tel', '')
        print(tel)
        address = request.POST.get('address', '')
        photo = request.POST.get('photo', '')
        # For now.
        sponsors = Sponsors.objects.get_or_create(
            name=name,
            logo=photo,
            tel=tel,
            direccion=address
        )
        sponsors = Sponsors.objects.get(
            name=name,
            logo=photo,
            tel=tel,
            direccion=address
        )
        return HttpResponseRedirect(
            "/add_sponsorship/" +
            str(event_id) +
            "/" + str(sponsors.id)
        )
    if ev.user is not request.user:
        messages.add_message(
            request, messages.ERROR,
            'Do not try to fool me, choose an event that is yours',
            extra_tags="danger"
        )
        return general_create(
        request,
        event_id,
        Sponsorship,
        SponsorshipCreateForm,
        'sponsorsManager/sponsorship_create_form.html',
        sponsors_id
    )


def sponsorship(request, instance_id, action):
    sponsorship = Sponsorship.objects.get(id=instance_id)
    event = Event.objects.get(Sponsorships=sponsorship)
    if event.user == request.user:
        redirect = "/events/" + str(event.id) + "/sponsorships/"
        if action == 'cancel':
            add_to_log(request, "Canceled Sponsorship with " +
                       str(sponsorship.sponsor) +
                       " from event " +
                       str(sponsorship.event))
            sponsorship.active = False
            sponsorship.save()
            return HttpResponseRedirect(redirect)
        if action == 'finish':
            add_to_log(request, "Finished Sponsorship with " +
                       str(sponsorship.sponsor) +
                       " from event " +
                       str(sponsorship.event))
            print('holi')
            sponsorship.finished = True
            sponsorship.save()
            return HttpResponseRedirect(redirect)
        if action == 'reactivate':
            add_to_log(request, "Reactivated Sponsorship with " +
                       str(sponsorship.sponsor) +
                       " from event " +
                       str(sponsorship.event))
            sponsorship.active = True
            sponsorship.finished = False
            sponsorship.save()
            return HttpResponseRedirect(redirect)
        elif action == 'detail':
            return render(request, "sponsorsManager/sponsorship_detail.html",
                          {'sponsorship': sponsorship,
                           'event': event}
                          )
    else:
        return HttpResponseRedirect('/404')


def send_emails(request):
    if request.method == 'GET':
        all_users = UserProfile.objects.all()
        for current_user in all_users:
            email_to = current_user.user.email
            email_from = 'no-reply@hey-sponsors.com'
            subject = 'Your weekly reminder'
            content = """
            <head>
              <style>
                 #email {
                   background-image:url("http://static2.wikia.nocookie.net/__cb20131129111846/neoxadventures/es/images/d/d1/Fondogif.jpg");
                   background-color:#336699;
                  @import url(http://fonts.googleapis.com/css?family=Merienda);
                 }
              </style>
            </head>
            <body>
             <div style="background:url('https://ci4.googleusercontent.com/proxy/mPjLVWw5-6QqIzGSKnU6B1Sp1WQQzTmYxLHG6qCND_jEv6iIkvJQpHEqnP0dDal3K6AUi7ThHcqx6B2XWcZcjQZWnxWskXn2FJLhZN0x3hNGKnnbwXk=s0-d-e1-ft#http://www.gstatic.com/android/market_images/email/email_top.png') no-repeat;width:100%;min-height:75px;display:block">

                <div style="padding-top:30px;padding-left:50px;padding-right:50px">
                    <img src="http://s29.postimg.org/u7detfhab/logo.png"  height="80" width="80" alt="Google Play"  align="middle" style="border:none">
                </div>

            </div>
            <div style="background:url('https://ci6.googleusercontent.com/proxy/Y6T6600sZwPUq5_OV_GKwVBk1bacpj8ZrlMaZjpK460x6sJpVMAUgvQtsVOA9zKEvgC6ODTZy7Rj-kTbTXnHo_N7D91xPP8GKvIgiRSHWiazm9VeNpo=s0-d-e1-ft#http://www.gstatic.com/android/market_images/email/email_mid.png') repeat-y;width:100%;display:block">
                <div style="padding-left:50px;padding-right:50px; padding-bottom:1px">
                    <div style="border-bottom:1px solid #ededed"></div>

            <h1>Hello again from Hey Sponsors!</h1>"""
            all_events = current_user.user.Events.all()
            print(datetime.now())
            filtered_events = all_events.order_by('date').filter(
                date__gte=datetime.now(),
                finished=False,
                active=True
            )[:3]
            if filtered_events.count() > 0:
                content += """These are your next events. <br>Have you contacted
                all your sponsors to make sure you are on time?
                <br />"""
                for current_event in filtered_events:
                    content += '<br/><hr><br/>'
                    content += 'Event name: ' + current_event.name + '<br>'
                    content += 'Date: ' + \
                        current_event.date.strftime("%d/%m/%Y")
                    content += '<br />'
                    if current_event.Needs.count() > 0:
                        content += "Needs: <br /><ul>"
                        for current_need in current_event.Needs.all():
                            content += '<li>' + current_need.name + '</li>'
                        content += '</ul>'
                    if current_event.Sponsorships.count() > 0:
                        content += 'Your sponsorships: '
                        all_sponsorships = current_event.Sponsorships.all()
                        for current_sponsorship in all_sponsorships:
                            if current_sponsorship.active is True and current_sponsorship.finished is False:
                                content += "<br />Sponsor: "
                                content += current_sponsorship.sponsor.name
                                content += "<br />Benefits: "
                                content += current_sponsorship.benefits.name
                                content += "<br />Concessions: "
                                content += current_sponsorship.concesions.name
                                content += "<br />"
                content += """
                </div>

                </div>
                <div style="background:url('https://ci5.googleusercontent.com/proxy/u6KYrquoddKACxnOzJ_0lN61heutVpw6mvCoYm12429bUiIixNVcgybrhdlhejL3Wt_3e-Z40wScTl6vSA4PJCyVv36WJtiqQKPkLLgp0eptolrfhCwmolk=s0-d-e1-ft#http://www.gstatic.com/android/market_images/email/email_bottom.png') no-repeat;width:100%;min-height:50px;display:block">
                </div>

                </body>
                """
                print(content)
                msg = EmailMessage(subject, content, to=[email_to])
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()

            # email.send()

    return index(request)
