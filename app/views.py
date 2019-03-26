from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Stop
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from app.static.app.sampledata import aikataulut
import datetime

# Tkl API
# user token: aleksilehmus
# token passphrase: ohsiha123

def HomePageView(request):
        oma_pysakki = request.user.profile.pysakki
        kello_nyt_str = str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute)
        kello_nyt = int(kello_nyt_str)
        seuraavat_linjat = []
        oma_aikataulu = {}
        if oma_pysakki in aikataulut:
                oma_aikataulu = aikataulut[oma_pysakki]
                for aika in oma_aikataulu:
                        if int(aika) > kello_nyt:
                                seuraavat_linjat.append(aika+" - "+oma_aikataulu[aika])
                        if len(seuraavat_linjat) == 5:
                                break
        context = {
                'aikataulut': aikataulut,
                'oma_pysakki': oma_pysakki,
                'oma_aikataulu': oma_aikataulu,
                'kello_nyt': kello_nyt,
                'seuraavat_linjat': seuraavat_linjat
        }

        return render(request, 'index.html', context)

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