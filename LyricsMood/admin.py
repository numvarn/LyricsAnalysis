from django.contrib import admin
from .models import Artists, Polar, Lyrics

class ArtistsAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class LyricsAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'polar', 'year')
    search_fields = ('title', 'artist__name', 'polar__polar')
    list_filter = ('polar__polar',)

# Register your models here.
admin.site.register(Polar)
admin.site.register(Artists, ArtistsAdmin)
admin.site.register(Lyrics, LyricsAdmin)