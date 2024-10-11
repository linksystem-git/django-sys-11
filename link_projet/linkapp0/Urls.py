from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from .views import * 

def is_superuser(user):
    return user.is_superuser

urlpatterns = [
    path('admin/', user_passes_test(is_superuser)(admin.site.urls)),
    path('', login_view, name='connexion'),  # Page de connexion, sans login_required

    # Ajout de login_required à toutes les autres vues
    path('home/', login_required(home), name='home'),  
    path('Data/', login_required(datas), name='datas'),  
    path('dossier/', login_required(page_dossiers), name='page_dossiers'),
    path('prospects/', login_required(page_prospects), name='page_prospects'),
    path('suivie/', login_required(suivie), name='suivie'),
    path('profile/', login_required(profiles), name='profiles'),  
    path('planning/', login_required(planning), name='planning'),   
    path('clients/', login_required(page_clients), name='page_clients'), 
    path('update_prospect/', login_required(views.edit_prospect), name='edit_prospect'),
    path('delete_prospect/<int:prospect_id>/', login_required(views.delete_prospect), name='delete_prospect'),

    #----------------------gestion dossier------------------------------------------
    path('supprimer-dossier/<int:dossier_id>/', login_required(supprimer_dossier), name='supprimer_dossier'),
    path('modifier_dossier/', login_required(views.modifier_dossier), name='modifier_dossier'),

    #----------------------gestion client--------------------------------------------------
    path('supprimer_client/<int:client_id>/', login_required(views.supprimer_client), name='supprimer_client'),

    #----------------------gestion incident------------------------------------------
    path('incidents/supprimer/<int:incident_id>/', login_required(supprimer_incident), name='supprimer_incident'),
    path('modifier_incident/<int:incident_id>/', login_required(views.modifier_incident), name='modifier_incident'),

    #----------------------gestion data------------------------------------------
    path('data/create/', login_required(views.data_create), name='data_create'),
    path('delete_data/', login_required(views.delete_data), name='delete_data'),
    path('edit_data/', login_required(views.edit_data), name='edit_data'),

    #---------------------deconnexion----------------------------------------
    path('deconnexion/', login_required(logout_view), name='logout'),
]
