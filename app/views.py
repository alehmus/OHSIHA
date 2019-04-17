from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Stop
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
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
                if len(h) == 1:
                        h = "0"+h
                kello_nyt = f'{h}:{min}'
                oma_pysakki = request.user.profile.pysakki
                oma_linja = request.user.profile.linja
                
                seuraavat_linjat = []
                seuraava_lähtö = []
                url = f'http://api.publictransport.tampere.fi/prod/?user=aleksilehmus&pass=ohsiha123&code={oma_pysakki}&request=stop'
                r = requests.get(url)
                dep = r.json()[0]["departures"]

                for line in dep:
                        lähtö_hm = line["time"]
                        if len(lähtö_hm) == 3:
                                lähtö_hm = "0" + lähtö_hm
                        lähtö_min = int(lähtö_hm[0:2])*60 + int(lähtö_hm[2:4])
                        kello_min = int(kello_nyt[0:2])*60 + int(kello_nyt[3:5])
                        odotus = lähtö_min - kello_min
                        linja = f'{line["code"]}: {lähtö_hm[0:2]}:{lähtö_hm[2:4]} ->'
                        seuraavat_linjat.append([linja, odotus])
                        if len(seuraava_lähtö) == 0 and oma_linja == line["code"]:
                                seuraava_lähtö = [line["code"], odotus]
                if len(seuraava_lähtö) == 0:
                        seuraava_lähtö = ['ei lähtöjä', 0]

                if request.method == 'POST':
                        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
                        if p_form.is_valid():
                                pysakkinimi = p_form.cleaned_data.get('pysakki')
                                if len(Stop.objects.filter(name=pysakkinimi)) == 0:
                                        messages.error(request, f'Pysäkkiä {pysakkinimi} ei ole olemassa')
                                        return redirect('kotisivu')
                                p_form.save()
                                messages.success(request, f'Tiedot päivitetty!')
                                return redirect('kotisivu')
                                
                else:
                        p_form = ProfileUpdateForm(instance=request.user.profile)


                context = {
                        'oma_pysakki': oma_pysakki,
                        'kello_nyt': kello_nyt,
                        'seuraavat_linjat': seuraavat_linjat,
                        'seuraava_lähtö': seuraava_lähtö,
                        'p_form': p_form,
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
                        pysakkinimi = p_form.cleaned_data.get('pysakki')
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