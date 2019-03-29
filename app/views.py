from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Stop
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, StopUpdateForm
import datetime, json, requests

# Tkl API
# user token: aleksilehmus
# token passphrase: ohsiha123

def HomePageView(request):
        if request.user.is_authenticated:
                min = str(datetime.datetime.now().minute)
                h = str(datetime.datetime.now().hour)
                if len(min) == 1:
                        min = "0"+min
                kello_nyt = f'{h}{min}'
                omat_pysakit = [
                        request.user.profile.pysakki1,
                        request.user.profile.pysakki2,
                        request.user.profile.pysakki3
                ]
                p_v = request.user.profile.pysakkivalinta
                oma_pysakki = omat_pysakit[p_v]
                seuraavat_linjat = []

                url = f'http://api.publictransport.tampere.fi/prod/?user=aleksilehmus&pass=ohsiha123&code={oma_pysakki}&request=stop'
                r = requests.get(url)
                dep = r.json()[0]["departures"]

                for line in dep:
                        odotus = int(line["time"]) - int(kello_nyt)
                        linja = f'{line["code"]}: {line["time"]} ->'
                        seuraavat_linjat.append([linja, odotus])

                if request.method == 'POST':
                        s_form = StopUpdateForm(request.POST, instance=request.user.profile)
                        if s_form.is_valid():
                                p_valinta = s_form.cleaned_data.get('pysakkivalinta')
                                oma_pysakki = omat_pysakit[p_valinta]
                                s_form.save()
                                messages.success(request, f'{oma_pysakki} vaihdettu pysäkiksi')
                                return redirect('kotisivu')
                else:
                        s_form = StopUpdateForm()

                context = {
                        'omat_pysakit': omat_pysakit,
                        'oma_pysakki': oma_pysakki,
                        'kello_nyt': kello_nyt,
                        'seuraavat_linjat': seuraavat_linjat,
                        's_form': s_form,
                        'p_v': p_v
                }

                return render(request, 'index.html', context)
        else:
                return render(request, 'index.html')

def RegisterView(request):
        if request.method == 'POST':
                form = UserRegisterForm(request.POST)
                if form.is_valid():
                        form.save()
                        username = form.cleaned_data.get('username')
                        messages.success
                        (request, f'{username} käyttäjätunnus luotu! Kirjaudu sisään')
                        return redirect('login')
        else:
                form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})


def SaveStop():
        url = '/Users/aleksilehmus/Documents/Koulu/TLO/OHSIHA/harkka/projekti/app/static/app/stopdata.txt'
        f = open(url, "r", encoding='utf-8-sig')
        for line in f:
                osat = line.split("/")
                stop = Stop.objects.create()
                stop.name = osat[0]
                stop.id_2 = osat[1]
                stop.save()

def ListStops():
        url = '/Users/aleksilehmus/Documents/Koulu/TLO/OHSIHA/harkka/projekti/app/static/app/stopdata.txt'
        f = open(url, "r", encoding='utf-8-sig')
        stops = {}
        for line in f:
                osat = line.split("/")
                stops[osat[0]] = osat[1].rstrip('\n')
        return stops

@login_required
def ProfileView(request):
        if request.method == 'POST':
                u_form = UserUpdateForm(request.POST, instance=request.user)
                p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                        pysakkinimi = p_form.cleaned_data.get('pysakki1')
                        if len(Stop.objects.filter(name=pysakkinimi)) == 0:
                                messages.error(request, f'Pysäkkiä {pysakkinimi} ei ole olemassa')
                                return redirect('profile')
                        u_form.save()
                        p_form.save()
                        messages.success(request, f'Profiilin tiedot päivitetty!')
                        return redirect('profile')
        else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                
        context = {
                'u_form': u_form,
                'p_form': p_form
        }
        return render(request, 'profile.html', context)