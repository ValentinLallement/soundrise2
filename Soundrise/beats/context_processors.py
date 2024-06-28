from django.shortcuts import get_object_or_404
from .models import Beats
from .utils import get_current_beat
# Assuming you have a Beat model with audio_file_url field
def audio_processor(request):
    current_beat = get_current_beat(request)
    audio_player_state = {}

    # Check if there's a currently playing beat based on URL parameters (replace with your logic)
    beat_id = request.GET.get('beat_id')
    if beat_id:
        current_beat = get_object_or_404(Beats, pk=beat_id)

    # Update audio player state based on current beat
    if current_beat:
        audio_player_state = {
            'playing': True,  # Set playing to true if a beat is playing
            'currentTime': 0,  # Initialize current playback time
            'duration': current_beat.duration,  # Assuming duration is a field in your model
        }

    return {'current_beat': current_beat, 'audio_player_state': audio_player_state}