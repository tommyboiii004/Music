from django.contrib import admin
from .models import Song, User, WatchLater

admin.site.register(Song)
admin.site.register(User)
admin.site.register(WatchLater)