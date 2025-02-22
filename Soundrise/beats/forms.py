from django import forms
from .models import Beats

class BeatForm(forms.ModelForm):
    class Meta:
        model = Beats
        fields = ['title', 'genre', 'duration', 'price', 'cover_image', 'audio_file','description','BPM']

    def clean_audio_file(self):
        audio_file = self.cleaned_data['audio_file']
        if audio_file:
            content_type = audio_file.content_type.split('/')[0]
            if content_type not in ['audio']:
                raise forms.ValidationError('File type is not supported. Please upload an audio file.')
        return audio_file
    

from beats.models import Playlist, Beats  # Assuming your models are in a folder named 'beats'

class AjouterTitreForm(forms.ModelForm):
    beat = forms.ModelChoiceField(queryset=Beats.objects.all(), label='Beat à ajouter')
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.filter(lu=False), label='Playlist')

    class Meta:
        model = Playlist
        fields = ['beat', 'playlist']