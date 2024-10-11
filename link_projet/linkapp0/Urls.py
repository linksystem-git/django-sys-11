# urls.py

from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from .views import * 

def is_superuser(user):
    return user.is_superuser

urlpatterns = [
    path('admin/', user_passes_test(is_superuser)(admin.site.urls)),
    path('', login_view, name='connexion'), 
    path('home/', home, name='home'),  
    path('Data/', datas, name='datas'),  
    path('dossier/', page_dossiers, name='page_dossiers'),
    path('prospects/', page_prospects, name='page_prospects'),
    path('suivie/', suivie, name='suivie'),
    path('profile/', profiles, name='profiles'),  
    path('planning/', planning, name='planning'),   
    path('clients/', page_clients, name='page_clients'), 
    path('update_prospect/', views.edit_prospect, name='edit_prospect'),
    path('delete_prospect/<int:prospect_id>/', views.delete_prospect, name='delete_prospect'),

    #----------------------gestion dossier------------------------------------------
    path('supprimer-dossier/<int:dossier_id>/', supprimer_dossier, name='supprimer_dossier'),
     path('modifier_dossier/', views.modifier_dossier, name='modifier_dossier'),
    #----------------------gestion client--------------------------------------------------
    path('supprimer_client/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
    #----------------------gestion incident------------------------------------------
    path('incidents/supprimer/<int:incident_id>/', supprimer_incident, name='supprimer_incident'),  # URL pour supprimer un incident
    path('modifier_incident/<int:incident_id>/', views.modifier_incident, name='modifier_incident'),
    #----------------------gestion data------------------------------------------
    path('data/create/', views.data_create, name='data_create'),
    path('delete_data/', views.delete_data, name='delete_data'),
    path('edit_data/', views.edit_data, name='edit_data'),

    #---------------------deconnexion----------------------------------------
    path('deconnexion/', logout_view, name='logout'),
    

]
