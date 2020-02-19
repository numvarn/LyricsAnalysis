from django.urls import path
from .views import Home, Login, Logout, Sigup, LyricsAllPage, ArtistAllPage, LyricsPage, ArtistPage

urlpatterns = [
    path('', Home, name='home'),
    path('users/login/', Login, name='login'),
    path('users/logout/', Logout, name='logout'),
    path('users/sigup/', Sigup, name='sigup'),
    path('lyrics/', LyricsAllPage, name='lyrics_all'),
    path('lyrics/<int:id>', LyricsPage, name='lyrics_page'),
    path('artists/<int:id>', ArtistPage, name='artist_page'),
    path('artists/', ArtistAllPage, name='artists_all'),
    # path('import/artist/', ImportArtist, name='import_atrist'),
    # path('import/lyrics/', ImportLyrics, name='import_lyrics'),
]