from datetime import date
from django.shortcuts import render, get_object_or_404

from player.models import Song, WatchLater
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm

def add_to_watch_later(request, song_id):
    if request.method == 'POST':
        user = request.user  
        song = Song.objects.get(pk=song_id)
        if(WatchLater.objects.filter(user=user, song=song).exists()):
            return redirect('watchlater')
        watch = WatchLater.objects.create(user=user, song=song)
        print(watch)
    return redirect('watchlater')  

def watch_later_list(request):
    user = request.user
    watch_later_songs = WatchLater.objects.filter(user=user)  # Optimize query with select_related
    context = {'watch_later_songs': watch_later_songs}
    return render(request, 'player/watchlater.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print("Done")
            if user:
                login(request, user)
                return redirect('home') 
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'player/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegistrationForm()
    return render(request, 'player/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
  songs = Song.objects.all()
  search_query = request.GET.get('query', '')
  if(request.user.is_anonymous == False):
    user = request.user
    watch_later_songs = WatchLater.objects.filter(user=user)
  else:
    watch_later_songs = []

  watch_later_list = []

  for watch_later in watch_later_songs:
      watch_later_list.append(watch_later.song)
  if search_query:
    songs = songs.filter(title__icontains=search_query)
  context = {'songs': songs, 'search_query': search_query, 'current_year': date.today().year, 'watch_later': watch_later_list}
  return render(request, 'player/home.html', context)

def about(request):
  return render(request, 'player/about.html')