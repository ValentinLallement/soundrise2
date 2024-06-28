from django.conf import settings
from django.urls import path , include
from . import views
from django.conf.urls.static import static 




app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('toggle_follow/<int:user_id>/<int:beat_id>/', views.toggle_follow, name='toggle_follow'),
    path('success/', views.success, name='success'),
    path('parametre/', views.parametre, name='parametre'),
    path('recherhche/', views.recherche, name='recherhce'),
    path('parametre/page/<str:page>/', views.parametre_onglet, name='parametre_onglet'),
    path('explore/',views.explore,name='explore'),
    path('search_beatmakers/',views.search_beatmakers,name='search_beatmakers'),
    path('detail_beat/<int:beat_id>/', views.detail_beat, name='detail_beat'),
    path('parametre/default',views.parametre_default,name='parametre_default'),
    path('create_card/',views.create_card,name='create_card'),
    path('create_paypal/',views.create_paypal,name='create_paypal'),
    path('parametre/activite-beat', views.parametre_like, name='parametre_like'),
    path('parametre/activite-fav', views.parametre_fav, name='parametre_fav'),
    path('parametre/activite-com', views.parametre_com, name='parametre_com'),
    path('parametre/historique-beat', views.historique_beat, name='historique_beat'),
    path('parametre/historique-artist', views.historique_artist, name='historique_artist'),
    path('parametre/historique-recherche', views.historique_recherche, name='historique_recherche'),
    path('parametre/transaction',views.parametre_transaction,name="parametre_transaction"),
    path('conversations', views.get_conversations, name='conversations'),
    path('conversation/<int:conversation_id>', views.get_messages, name='get_messages'),
    path('add_conversation/<int:participant1_id><int:participant2_id>', views.add_conversation, name='add_conversation'),
    path('create_conversation/<int:participant1_id><int:participant2_id>', views.create_conversation, name='create_conversation'),
    path('create_message', views.create_message, name='create_message'),
    path('pulse',views.pulse,name='pulse'),
    path('playlist/<int:id>/lire/', views.lire_titre, name='lire_titre'),
    path('playlist/<int:id>/supprimer/', views.supprimer_titre, name='supprimer_titre'),
    path('ajouter_titre/', views.topbar, name='ajouter_titre'),
    
    

    
    

    
]


