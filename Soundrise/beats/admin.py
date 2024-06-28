from django.contrib import admin
from .models import Beats  ,Playlist


class BeatsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'score', 'artist', 'genre', 'release_date', 'price')

    # Fields to filter the list by
    list_filter = ('genre', 'release_date', 'artist', 'score')

    # Fields to search by
    search_fields = ('title', 'artist__username', 'genre')


    # Fields to be edited inline
    fieldsets = (
        (None, {
            'fields': ('title', 'artist', 'genre', 'duration', 'release_date', 'price', 'BPM', 'description', 'views')
        }),
        ('Media', {
            'fields': ('cover_image', 'audio_file')
        }),
    )
def get_beats_display(self):
    return ", ".join([beat.title for beat in self.beats.all()])

from .admin import get_beats_display
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ( 'utilisateur', 'lu', 'position', get_beats_display,)  # Display title, user, listened (lu), position
    search_fields = ( 'utilisateur__username',)  # Search by title and username
      # Make user field read-only


    def __str__(self):
        return f"{self.titre} - {self.utilisateur}"
admin.site.register(Playlist, PlaylistAdmin)

admin.site.register(Beats, BeatsAdmin)
