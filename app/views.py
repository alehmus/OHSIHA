from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import blogi, Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, BlogForm, UserUpdateForm, ProfileUpdateForm
from app.static.app.sampledata import aikataulut
import datetime

# Tkl API
# user token: aleksilehmus
# token passphrase: ohsiha123

def HomePageView(request):
        posts = blogi.objects.all()
        oma_pysakki = request.user.profile.pysakki
        oma_aikataulu = aikataulut[oma_pysakki]
        kello_nyt_str = str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute)
        kello_nyt = int(kello_nyt_str)
        seuraavat_linjat = []
        for aika in oma_aikataulu:
                if int(aika) > kello_nyt:
                        seuraavat_linjat.append(aika+" - "+oma_aikataulu[aika])
                if len(seuraavat_linjat) == 5:
                        break
                        
        context = {
                'posts': posts,
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

def SampleView(request):
    blog = BlogForm()
    return render(request, 'sample.html', {'form': blog})

def SavePost(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            post = blogi.objects.create()
            post.name = data.get('name')
            post.text = data.get('text')
            post.save()
    return HttpResponseRedirect('/')

@login_required
def ProfileView(request):
        if request.method == 'POST':
                u_form = UserUpdateForm(request.POST, instance=request.user)
                p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
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