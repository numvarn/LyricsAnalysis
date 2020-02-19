from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Artists, Lyrics, Polar
import csv, io

# Create your views here.
def Home(request):
    context = {
        'title':'Lyrics Analysis System',
    }
    return render(request, 'home.html', context)
# -----------------------------------------------------------------------------
def LyricsAllPage(request):
    lyrics_obj = Lyrics.objects.all().order_by('year')

    context = {
        'title':'All Lyrics',
        'lyrics':lyrics_obj,
    }

    return render(request, 'lyrics_all.html', context)
# -----------------------------------------------------------------------------
def ArtistAllPage(request):
    artists_obj = Artists.objects.all().order_by('name')
    num_songs = []
    for artist in artists_obj:
        num_songs.append(Lyrics.objects.filter(artist=artist).count())

    context = {
        'title':'All Artists',
        'artists':artists_obj,
        'songs':num_songs,
    }

    return render(request, 'artists_all.html', context)
# -----------------------------------------------------------------------------
def LyricsPage(request, id):
    lyric_obj = Lyrics.objects.get(id=id)
    context = {
        'title':lyric_obj.title,
        'lyric':lyric_obj,
    }
    return render(request, 'lyrics_page.html', context)
# -----------------------------------------------------------------------------
def ArtistPage(request, id):
    artist_obj = Artists.objects.get(id=id)
    lyrics_obj = Lyrics.objects.filter(artist=artist_obj)
    context = {
        'title':artist_obj.name,
        'artist':artist_obj,
        'lyrics':lyrics_obj,
    }
    return render(request, 'artists_page.html', context)
# -----------------------------------------------------------------------------
# User Login
def Login(request):
    if request.method == 'POST':
        user = authenticate(
                    username=request.POST.get('user'),
                    password=request.POST.get('password')
                )
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'This account has been disabled!')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Error wrong username/password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
# -----------------------------------------------------------------------------
def Logout(request):
    messages.error(request, 'User has been loged out')
    logout(request)
    return redirect('/users/login/')
# -----------------------------------------------------------------------------
def Sigup(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        pass1 = request.POST.get('password1')

        if CheckUserExist(name, email):
            user = User.objects.create_user(
                        username=name,
                        first_name=firstname,
                        last_name=lastname,
                        email=email,
                        password=pass1,
                    )
            if user is not None:
                messages.error(request, 'User has been created.')
                return redirect('/users/login')
        else:
            messages.error(request, 'Username or Email is Already Exist')
            return render(request, 'register.html')
        return render(request, 'register.html')
    else:
        return render(request, 'register.html')
# -----------------------------------------------------------------------------
# Check User or Email is Already Exist
def CheckUserExist(name, email):
    user = User.objects.filter(
                Q(username__icontains=name) |
                Q(email__icontains=email)
            )
    if len(user) != 0:
        return False
    else:
        return True
# -----------------------------------------------------------------------------
# Import User From CSV File
@user_passes_test(lambda u: u.is_superuser)
def ImportArtist(request):
    context = {
        'title':'Lyrics Analysis System'
    }

    with open('/Users/phisan/Desktop/04.lyrics_clean_atist_name.txt') as f:
        for artist in f.readlines():
            artist = artist.replace('\n', '')
            artist_obj = Artists(name=artist)
            artist_obj.save()
        
    return render(request, 'home.html', context)
    # -----------------------------------------------------------------------------
# Import User From CSV File
@user_passes_test(lambda u: u.is_superuser)
def ImportLyrics(request):
    context = {
        'title':'Lyrics Analysis System'
    }

    with open('/Users/phisan/Desktop/03.lyrics_clean_atist_name.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if len(row[10]) > 4:
                row[10] = 2554

            lyric_obj = Lyrics(
                title = row[0],
                artist = Artists.objects.get(name=row[1]),
                polar = Polar.objects.get(polar=row[2]),
                chorus = row[3],
                hook = row[4],
                lead = row[5],
                year = row[10],
            )
        
            lyric_obj.save()
        
    return render(request, 'home.html', context)