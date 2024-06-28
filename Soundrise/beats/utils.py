from django.shortcuts import get_object_or_404
from .models import Beats
def get_current_beat(request):
    # Retrieve the beat ID from session data (replace with your chosen logic)
    beat_id = request.session.get('current_beat_id')

    if beat_id:
        try:
            # Fetch the beat object from the database
            current_beat = get_object_or_404(Beats, pk=beat_id)
            return current_beat
        except ObjectDoesNotExist:
            # Handle case where beat ID in session is invalid
            pass

    # Return None if no current beat is found
    return None