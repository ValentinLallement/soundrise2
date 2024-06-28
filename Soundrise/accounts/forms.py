from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , Conversation 



class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'country', 'password1', 'password2']

class ParametreForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name','username', 'tel','email', 'password','country']



class ParametreProForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=['mail_pro']


class ConversationForm(forms.ModelForm):
    title = forms.CharField(label="Titre de la conversation", max_length=255)
    participants = forms.ModelMultipleChoiceField(label="Participants", queryset=CustomUser.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        # Assuming you have the `participant1` and `participant2` variables available
        super().__init__(*args, **kwargs)

        if 'participant1' in kwargs:
            self.fields['participants'].initial = [kwargs['participant1'], kwargs['participant2']]

    class Meta:
        model = Conversation
        fields = [ 'participants','title']

from beats.models import Playlist, Beats  # Assuming your models are in a folder named 'beats'

class AjouterTitreForm(forms.ModelForm):
    beat = forms.ModelChoiceField(queryset=Beats.objects.all(), label='Beat à ajouter')
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.filter(lu=False), label='Playlist')

    class Meta:
        model = Playlist
        fields = ['beat', 'playlist']