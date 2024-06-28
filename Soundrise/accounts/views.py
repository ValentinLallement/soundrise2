import os, glob
from pathlib import Path
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ParametreForm, ParametreProForm, RegisterForm
from accounts.models import CustomUser
from transaction.forms import CompteBancaireForm , PayPalAccountForm
from django.contrib.auth.decorators import login_required
from beats.models import Beats
from django.db.models import Q
from beats.utils import get_current_beat
from beats.context_processors import audio_processor



BASE_DIR = Path(__file__).resolve().parent.parent

def login_view(request):
    error_message = ""
    register_form = RegisterForm()

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:success')  # Redirect to home page after login
        else:
            error_message = "Invalid username or password. Please try again."
            

    return render(request, 'pages/login.html', {'form': register_form, 'error_message': error_message})

def register_view(request):
    print(os.path.join(BASE_DIR, 'files', 'static/'))
    register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('content/home/', permanent=True)
    return render(request, 'pages/register.html', {'form': register_form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def get_audio_file(beat):
    media_root = settings.MEDIA_ROOT
    beat_directory = os.path.join(media_root, 'audio', 'beats')
    audio_files = glob.glob(os.path.join(beat_directory, '*.mp3'))
    
    for file_path in audio_files:
        if os.path.basename(file_path) == os.path.basename(beat.audio_file.name):
            relative_path = os.path.relpath(file_path, media_root)
            return os.path.join(settings.MEDIA_URL, relative_path)
    
    return None

@login_required
def profile(request, username=None):
    current_beat = get_current_beat(request)

    current_user = request.user
    if username is None:
        user = request.user  # Logged-in user's profile
    else:
        user = get_object_or_404(CustomUser, username=username)  # Profile of the user with given username
    
    uploaded_beats = Beats.objects.filter(artist=user)
    
    for beat in uploaded_beats:
        beat.audio_file_url = get_audio_file(beat)
        
    is_followed = user.is_followed_by_user(request.user)
    follower_count = user.get_follower_count()
    following_count = user.get_following_count()
    
    context = {
        'user_profile': user,
        'uploaded_beats': uploaded_beats,
        'is_followed': is_followed,
        'follower_count': follower_count,
        'following_count':following_count,
        'current_user':current_user,
        'current_beat': current_beat,
        'audio_player_state': audio_processor(request)['audio_player_state'],
        'request': request,
    }
    print(current_beat)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    return render(request, 'pages/profile.html', context)


def success(request):
    return render(request, 'pages/success.html')



def parametre_about(request):
    return render(request,'pages/parametre/about.html')

def parametre_cookie(request):
    return render(request,'pages/parametre/cookie.html')

def parametre_confidentiality(request):
    return render(request,'pages/parametre/confidentiality.html')

def recherche(request):
    return render(request,'pages/recherche.html')


@login_required
def parametre(request):
    if request.method == 'POST':
        form = ParametreForm(request.POST,instance=request.user)
        form2 = ParametreProForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
                  
        elif form2.is_valid():
            form2.save()
    
    return render(request, 'pages/parametre.html')


@login_required
def parametre_onglet(request, page):
    print('page URLis: pages/parametre/'+page+'.html')
    if page == 'tableau':
        user = request.user 
        uploaded_beats = Beats.objects.filter(artist=user)
        context = {'uploaded_beats':uploaded_beats}
    else:
        context = {}
    return render(request, 'pages/parametre/'+page+'.html', context)
    
def explore(request):
    search_term = request.GET.get('search')
    current_beat = get_current_beat(request)

    if search_term is None:
        search_term = ""
    error = None
    filtered_models = Beats.objects.all()
    resetButton = False
    
    # Applying search filter
    if search_term:
        filtered_models = filtered_models.filter(title__icontains=search_term)
        if not filtered_models.exists():
            error = f"No beats corresponding to: {search_term}"
    
    # Applying price filter
    cursor_price = request.GET.get('cursor_price')
    if cursor_price:
        filtered_models = filtered_models.filter(price__lte=cursor_price)
        resetButton = True
    
    # Applying genre filter
    genre = request.GET.get('genre')
    if genre:
        filtered_models = filtered_models.filter(genre__icontains=genre)
        resetButton = True
    
    # Applying artist filter
    artist = request.GET.get('artist')
    if artist:
        filtered_models = filtered_models.filter(artist__username__icontains=artist)
        resetButton = True
    
    # Applying release year filter
    release_date = request.GET.get('release_date')
    if release_date:
        filtered_models = filtered_models.filter(release_date=release_date)
        resetButton = True
    
    # Applying sort order
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'trending':
        filtered_models = filtered_models.order_by('-score')
        resetButton = True
    if sort_by == 'price':
        filtered_models = filtered_models.order_by('-price')
        resetButton = True
    elif sort_by == 'price (reversed)':
        filtered_models = filtered_models.order_by('price')
        resetButton = True
    elif sort_by == 'latest':
        filtered_models = filtered_models.order_by('-release_date')
        resetButton = True
    elif sort_by == 'oldest':
        filtered_models = filtered_models.order_by('release_date')
        resetButton = True
    # Add more sorting options as needed
    
    # Handling descending order
    order = request.GET.get('order')
    if order == 'desc':
        filtered_models = filtered_models.reverse()
    
    # Handle like/unlike button form submissions
    if request.method == 'POST':
        if request.user.is_authenticated:
            beat_id = request.POST.get('beat_id')  # Assuming you have a hidden input in the form with beat_id
            beat = get_object_or_404(Beats, id=beat_id)
            if 'like_button' in request.POST:
                if beat.add_like(request.user):
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user already liked the beat
                    pass  # You can redirect or render an error message
            elif 'unlike_button' in request.POST:
                if beat.remove_like(request.user):
                    # Handle successful like removal
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user hasn't liked the beat
                    pass  # You can redirect or render an error message
        else:
            # Handle case where user is not authenticated
            pass  # You can redirect or render a message to log in
    
    # Get all unique artist names from the filtered beats
    artist_ids = filtered_models.values_list('artist', flat=True).distinct()
    
    # Get user data for all these artists
    users = CustomUser.objects.filter(id__in=artist_ids)
    user_dict = {user.username: {'user': user, 'rank': user.rank} for user in users}
    
    # Prepare audio file URLs
    for beat in filtered_models:
        beat.audio_file_url = get_audio_file(beat)  # Assuming get_audio_file is a function to get audio file URL
    
    top_3_beats = sorted(filtered_models, key=lambda b: b.score, reverse=True)[:3]
    top_3_scores = [beat.score for beat in top_3_beats]

    context = {
        'beats': filtered_models,
        'search_term': search_term,
        'error': error,
        'user_dict': user_dict,
        'sort_by': sort_by,
        'genre': genre,
        'artist': artist,
        'release_date': release_date,
        'resetButton': resetButton,
        'top_3_scores':top_3_scores,
        'current_beat': current_beat,
        'audio_player_state': audio_processor(request)['audio_player_state'],
        'request': request,
        
    }
    
    
    return render(request, 'pages/explore.html', context)


@login_required
def toggle_follow(request, user_id, beat_id):
    if beat_id == 0:
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        
        # Logic to toggle follow/unfollow
        if current_user in user_to_follow.followers.all():
            user_to_follow.followers.remove(current_user)
        else:
            user_to_follow.followers.add(current_user)
        
        # Redirect back to the detail_beat page with the correct beat_id
        return redirect('accounts:profile', username=user_to_follow.username)
    
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    current_user = request.user
    
    # Logic to toggle follow/unfollow
    if current_user in user_to_follow.followers.all():
        user_to_follow.followers.remove(current_user)
    else:
        user_to_follow.followers.add(current_user)
    
    # Redirect back to the detail_beat page with the correct beat_id
    return redirect('accounts:detail_beat', beat_id=beat_id)


def search_beatmakers(request):
    user = request.user
    is_followed = user.is_followed_by_user(request.user)
    search_term = request.GET.get('search')
    error = None
    filtered_models = CustomUser.objects.all()  # Default queryset with all beatmakers

    if search_term:
        # Filter the model list using the search term
        filtered_models = CustomUser.objects.filter(
            Q(username__icontains=search_term)
        )

        if not filtered_models.exists():
            error = f"No beatmakers corresponding to: {search_term}"
            search_term = ""
    else:
        search_term = ""

    # Add logic to fetch beats for each beatmaker
    annotated_models = []
    
    for beatmaker in filtered_models:
        # Use related_name 'uploaded_beats' defined in Beats model
        beats = beatmaker.uploaded_beats.all()
        for beat in beats:
            beat.audio_file_url = get_audio_file(beat)
        annotated_models.append({
            'beatmaker': beatmaker,
            'beats': beats,
            
        })
    
    context = {
        'annotated_models': annotated_models,  # Use annotated_models instead of beatmakers
        'search_term': search_term,
        'error': error,
        'beatmakers': filtered_models,
        'is_followed':is_followed,
    }

    return render(request, 'pages/search_beatmakers.html', context)


def detail_beat(request, beat_id):
    beat = get_object_or_404(Beats, id=beat_id)
    user = beat.artist
    is_followed = user.is_followed_by_user(request.user)
    follower_count = user.get_follower_count()
    following_count = user.get_following_count()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'like_button' in request.POST:
                if beat.add_like(request.user):
                    # Handle successful like addition
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user already liked the beat
                    pass  # You can redirect or render an error message
            elif 'unlike_button' in request.POST:
                if beat.remove_like(request.user):
                    # Handle successful like removal
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user hasn't liked the beat
                    pass  # You can redirect or render an error message
        else:
            # Handle case where user is not authenticated
            pass  # You can redirect or render a message to log in

    context = {
        'beat': beat,
        'user': user,
        'is_followed': is_followed,
        'follower_count': follower_count,
        'following_count': following_count,
    }

    return render(request, 'pages/detail_beat.html', context)

def parametre_tableau(request):
    user = request.user
    uploaded_beats = Beats.objects.filter(artist=user)
    latest_model = uploaded_beats.latest('release_date')
    context = {
        'user':user,
        'latest_model':latest_model,
        
    }

    return render(request, 'pages/parametre/tableau', context)
    
def parametre_default(request):
    user = request.user
    follower_count = user.get_follower_count()
    context={
        'follower_count':follower_count,
    }
    return render(request, 'pages/parametre/default', context)


def parametre_transaction(request):
    return render(request, 'pages/parametre/transaction.html')


def parametre_like(request):
    user = request.user

    user_likes = []  # Initialize an empty list to store liked beats

    if user.is_authenticated:
        user_likes = Beats.objects.filter(likes=user)
    

    if request.method == 'POST':
        if request.user.is_authenticated:
            beat_id = request.POST.get('beat_id')  # Assuming you have a hidden input in the form with beat_id
            beat = get_object_or_404(Beats, id=beat_id)
            if 'like_button' in request.POST:
                if beat.add_like(request.user):
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user already liked the beat
                    pass  # You can redirect or render an error message
            elif 'unlike_button' in request.POST:
                if beat.remove_like(request.user):
                    # Handle successful like removal
                    pass  # You can redirect or render a success message
                else:
                    # Handle case where user hasn't liked the beat
                    pass  # You can redirect or render an error message
        else:
            # Handle case where user is not authenticated
            pass  # You can redirect or render a message to log in

    context = {
        'user': user,
        'user_likes': user_likes,
    }

    return render(request, 'pages/parametre/activite-beat.html', context)
def parametre_fav(request):
    user=request.user
    beats=Beats.objects.all()
    favs=None
    for beat in beats :
        if user.has_fav():
            favs.append(beat)
        else:
            pass
    context = {
            'user':user,
            'fav':favs,

        }

                
    return render(request,'pages/parametre/activite-fav.html',context)
def parametre_com(request):
    return render(request,'pages/parametre/activite-com.html')

def historique_beat(request):
     return render(request,'pages/parametre/historique-beat.html')
def historique_artist(request):
     return render(request,'pages/parametre/historique-artist.html')
def historique_recherche(request):
     return render(request,'pages/parametre/historique-recherche.html')

def create_paypal(request):
    if not request.user.is_authenticated:
        return redirect('login_views')  # Redirect to login if not authenticated
    paypal_account_form = PayPalAccountForm(request.POST or None)

    if paypal_account_form.is_valid():
        # Save PayPal account form
        paypal_account = paypal_account_form.save(commit=False)
        paypal_account.user = request.user
        paypal_account.save()

        # Redirect to specific success page for PayPal account
        return redirect('accounts:parametre_transaction')
    else:
        # Handle invalid forms
        context = {
            
            'paypal_account_form': paypal_account_form,
        }
        return render(request, 'pages/create_paypal.html', context)

def create_card(request):
    if not request.user.is_authenticated:
        return redirect('login_views')  # Redirect to login if not authenticated

    compte_bancaire_form = CompteBancaireForm(request.POST or None)
    

    if compte_bancaire_form.is_valid():
        # Save Compte Bancaire form
        compte_bancaire = compte_bancaire_form.save(commit=False)
        compte_bancaire.user = request.user
        compte_bancaire.save()

        # Redirect to specific success page for Compte Bancaire
        return redirect('accounts:parametre_transaction')

    

    else:
        # Handle invalid forms
        context = {
            'compte_bancaire_form': compte_bancaire_form,
            
        }
        return render(request, 'pages/create_card.html', context)
    
def message(request):
    return render(request, 'pages/message.html')


from django.contrib.auth import get_user_model
from .models import Conversation, Message 
from .forms import ConversationForm


def add_conversation(request, participant1_id, participant2_id):
    try:
        participant1 = CustomUser.objects.get(pk=participant1_id)
        participant2 = CustomUser.objects.get(pk=participant2_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "One or both participants do not exist.")
        return redirect('accounts:profile', participant1_id)  # Adjust URL name if needed

    if request.method == 'POST':
        conversationForm = ConversationForm(request.POST)
        conversationForm.save()
        if conversationForm.is_valid():
            conversation = conversationForm.save()  # Save the conversation first
            conversation.participants.add(participant1, participant2)
            conversation_id = conversation.id
            conversation.title = ('title')  # Assuming you want to set a default title
            conversation.save()

            context = {
                'conversation_id': conversation_id
            }

            return render(request, 'pages/message/conversation.html', context)

    # Pre-populate participants in the form instance manually
    pass
 
    return render(request, 'pages/message/add_conversation.html')
   

def create_conversation(request, participant1_id, participant2_id):
    context={
        'participant1_id':participant1_id,
        'participant2_id':participant2_id,

    }
    return render(request, 'pages/message/add_conversation.html', context)

def get_other_participant(self, user):
    """
    Retrouve l'autre participant d'une conversation.
    """
    return self.participants.exclude(id=user.id).only_one()

def get_conversations(request):
    current_user = request.user
    
    conversations = Conversation.objects.filter(participants=current_user)
    return render(request, 'pages/message/conversations.html', {'conversations': conversations})

def create_message(request,conversation_id):
    # Handle message creation logic if included in ConversationForm:
    if 'message' in request.POST:
        message_text = request.POST['message']
        message = Message.objects.create(conversation=Conversation.objects, content=message_text)
        conversation = Conversation.objects.get(pk=conversation_id)  # Assuming you have conversation_id
        


            
    return redirect('accounts:get_messages')


def get_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)

   
    context = {
        'conversation': conversation,
        # ... (Other context variables for messages, participants, etc.)
    }

    return render(request, 'pages/messages.html', context)

def get_messages(request, conversation_id):
    """
    Retrieves messages for a conversation and handles new message creation.

    Args:
        request (HttpRequest): The Django HTTP request object.
        conversation_id (int): The primary key of the conversation.

    Returns:
        HttpResponse: A rendered response containing conversation details and messages.
    """

    try:
        conversation = Conversation.objects.get(pk=conversation_id)
    except Conversation.DoesNotExist:
        messages.error(request, "Conversation not found.")
        return redirect('conversations:list')  # Adjust URL name if needed

    current_user = request.user

    # Efficiently filter messages for the current user (no changes needed)
    messages = conversation.messages.filter(participants__in=[current_user]).order_by('created_at')

    other_participant_username = None
    new_message = None

    if conversation.participants.count() == 2:  # Ensure two participants exist (no changes)
        other_participant = conversation.participants.exclude(pk=current_user).first()
        if other_participant:
            other_participant_username = other_participant.username

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            try:
                # Use the defined ForeignKey fields for sender and recipient
                new_message = Message.objects.create(
                    sender=current_user,
                    recipient=conversation.get_other_participant(current_user),
                    conversation=conversation,
                    body=body
                )
            except Conversation.DoesNotExist:  # Handle potential foreign key constraint error
                messages.error(request, "Conversation not found. Please try again.")
                return redirect('conversations:list')  # Redirect on error

    context = {
        'conversation': conversation,
        'messages': messages,
        'new_message': new_message,
        'other_participant_username': other_participant_username,
    }

    return render(request, 'pages/message/conversation.html', context)


def pulse(request):
    return render(request, 'pages/pulse.html')


from beats.models import Playlist, Beats  # Assuming your models are in a folder named 'beats'
from beats.forms import AjouterTitreForm  # Assuming you have a form for adding titles

@login_required  # Ensures user is logged in
def topbar(request):
    utilisateur = request.user

    # Try to get the next unplayed beat for the user
    playlist_item = Playlist.objects.filter(utilisateur=utilisateur, lu=False).order_by('position').first()

    if playlist_item:  # If there's a beat to add
        beat = playlist_item.beat  # Get the associated beat

        try:
            # Add the beat to the user's playlist (if not already there)
            playlist_item.playlist.beats.add(beat)
            playlist_item.save()
            message = 'Le beat a été ajouté à votre playlist.'  # Success message
        except Playlist.DoesNotExist:
            message = 'La playlist n\'existe pas.'  # Error message (unlikely)

        return redirect('topbar', messages=[message])  # Redirect with message
    else:
        message = 'Aucun beat disponible à ajouter.'  # No more beats to add message

    # No playlist items found or error - pass the message to the template
    playlist = Playlist.objects.filter(utilisateur=utilisateur, lu=False).order_by('position')
    titre_suivant = playlist.first() if not playlist else None

    return redirect(request, 'topbar', {
        'message': message,  # Pass the message to the template
        'playlist': playlist,
        'titre_suivant': titre_suivant,
    })

# Removed unnecessary code from the index view

def supprimer_titre(request, id):
    try:
        playlist_item = Playlist.objects.get(id=id)
        playlist_item.delete()
        message = 'Le beat a été supprimé de votre playlist.'  # Success message
    except Playlist.DoesNotExist:
        message = 'Le beat n\'existe pas dans votre playlist.'  # Error message

    return redirect('topbar', messages=[message])  # Redirect to topbar view

def lire_titre(request, id):
    try:
        playlist_item = Playlist.objects.get(id=id)
        playlist_item.lu = True
        playlist_item.save()

        utilisateur = request.user
        playlist_suivante = Playlist.objects.filter(utilisateur=utilisateur, lu=False, position__gt=playlist_item.position).order_by('position').first()
        titre_suivant = playlist_suivante.beat if playlist_suivante else None

        # Delete the beat after marking it as listened to
        playlist_item.beat.delete()

        return redirect('topbar', titre_suivant=titre_suivant)  # Redirect to topbar view
    except Playlist.DoesNotExist:
        message = 'Le beat n\'existe pas dans votre playlist.'
        return redirect('topbar', messages=[message])  # Redirect with message
