from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Rediriger vers la page d'accueil
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'pages-connexion.html')  # Rendre le template de connexion


def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion') 

def home(request):
    return render(request, 'index1.html',{'user': request.user})



def dossiers(request):
    return render(request, 'pages-dossier.html',{'user': request.user})

def prospect(request):
    return render(request, 'pages-prospects.html',{'user': request.user})

def suivie(request):
    return render(request, 'pages-prospects.html',{'user': request.user})



def profiles(request):
    return render(request, 'users-profile.html',{'user': request.user})

def clients(request):
    
    return render(request, 'pages-clients.html',{'user': request.user})

def planning(request):
    return render(request, 'pages-planning.html',{'user': request.user})




from django.shortcuts import render, redirect
from .models import Prospect
from .forms import ProspectForm
from django.contrib import messages

def page_prospects(request):
    # Récupération des prospects pour affichage
    prospects = Prospect.objects.all()

    # Si l'utilisateur soumet le formulaire
    if request.method == 'POST':
        form = ProspectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Enregistre le prospect
            messages.success(request, 'Prospect ajouté avec succès !')  # Message de succès
            return redirect('page_prospects')  # Recharge la même page
    else:
        form = ProspectForm()  # Nouveau formulaire

    return render(request, 'pages-prospects.html', {'prospects': prospects, 'form': form})


#================================================================================================
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Prospect

def delete_prospect(request, prospect_id):
    # Corriger l'utilisation du champ idprospect au lieu de id
    prospect = get_object_or_404(Prospect, idprospect=prospect_id)
    
    if request.method == 'DELETE':
        prospect.delete()
        return JsonResponse({'message': 'Prospect supprimé avec succès.'}, status=200)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

#================================================================================================

from .models import Data, Prospect



from django.shortcuts import render, redirect, get_object_or_404
from .models import Prospect

def edit_prospect(request):
    if request.method == 'POST' and request.POST.get('action') == 'modifier':
        prospect_id = request.POST.get('prospect_id')
        # On récupère l'objet prospect à partir de l'ID
        prospect = get_object_or_404(Prospect, idprospect=prospect_id)

        # On met à jour les informations avec les données du formulaire
        prospect.nom = request.POST.get('prospect')
        prospect.adresse = request.POST.get('adresse')
        prospect.contact = request.POST.get('contact')
        prospect.referant = request.POST.get('referant')
        prospect.contact_referant = request.POST.get('contact_referant')
        prospect.email = request.POST.get('email')
        prospect.date_depot = request.POST.get('date_depot')
        
        # On sauvegarde les modifications
        prospect.save()

        # Redirection après modification
        return redirect('page_prospects')

    # Rendre la page avec la liste des prospects (et possiblement d'autres données)
    prospects = Prospect.objects.all()
    context = {'prospects': prospects}
    return render(request, 'page_prospects.html', context)







#============================= pages dossiers ==========================
from django.shortcuts import render, redirect
from .models import Dossier, Prospect, Agent, Client
from .forms import DossierForm
from django.contrib import messages
from django.utils import timezone

def page_dossiers(request):
    dossiers = Dossier.objects.all()
    prospects = Prospect.objects.all()
    agents = Agent.objects.all()

    if request.method == 'POST':
        form = DossierForm(request.POST)
        if form.is_valid():
            # Normaliser les valeurs pour éviter les majuscules
            form.cleaned_data['service'] = form.cleaned_data['service'].lower()
            form.cleaned_data['statut'] = form.cleaned_data['statut'].lower()

            # Enregistrer les données normalisées dans le formulaire
            dossier = form.save(commit=False)
            dossier.service = form.cleaned_data['service']
            dossier.statut = form.cleaned_data['statut']
            dossier.save()

            # Vérifier le statut et créer un client si nécessaire
            if dossier.statut in ["signe_valide", "termine"]:
                prospect = dossier.idprospect
                # Vérifier si un Client existe déjà pour ce Prospect
                if not Client.objects.filter(idprospect=prospect).exists():
                    Client.objects.create(idprospect=prospect, date=timezone.now())

            messages.success(request, 'Dossier ajouté avec succès !')
            return redirect('page_dossiers')
        else:
            messages.error(request, 'Erreur lors de l\'ajout du dossier. Veuillez vérifier les informations saisies.')
    else:
        form = DossierForm()

    return render(request, 'pages-dossiers.html', {'dossiers': dossiers, 'form': form, 'prospects': prospects, 'agents': agents})


#-------------------------------suppression 

from django.http import JsonResponse
from .models import Dossier

def supprimer_dossier(request, dossier_id):
    if request.method == 'DELETE':
        try:
            # Utiliser iddossier au lieu de id
            dossier = Dossier.objects.get(iddossier=dossier_id)
            dossier.delete()  # Supprimer le dossier
            return JsonResponse({'status': 'success', 'message': 'Dossier supprimé avec succès.'}, status=200)
        except Dossier.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Dossier introuvable.'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


#--------------------------modification
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Dossier, Client
from django.utils import timezone

def modifier_dossier(request):
    if request.method == 'POST':
        iddossier = request.POST.get('iddossier')
        dossier = get_object_or_404(Dossier, iddossier=iddossier)

        # Mettre à jour les champs du Dossier
        dossier.titre_projet = request.POST.get('Projet')
        dossier.idprospect_id = request.POST.get('prospect')
        dossier.idagent_id = request.POST.get('Commercial')
        dossier.service = request.POST.get('Service')
        dossier.statut = request.POST.get('Statut')
        dossier.courrierreference = request.POST.get('courrierreference')
        dossier.description = request.POST.get('description')
        dossier.date_depot = request.POST.get('date_depot')
        dossier.date_relance = request.POST.get('date_relance')

        # Sauvegarder le Dossier avant de créer le Client
        dossier.save()

        # Vérifier le statut et créer un client si nécessaire
        if dossier.statut in ["signe_valide", "termine"]:
            prospect = dossier.idprospect
            # Vérifier si un Client existe déjà pour ce Prospect
            if not Client.objects.filter(idprospect=prospect).exists():
                Client.objects.create(idprospect=prospect, date=timezone.now())

        return JsonResponse({'success': True, 'message': 'Modification réussie'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

#======================================gestion client 

from django.shortcuts import render
from .models import Client, Prospect, Dossier

def page_clients(request):
    clients = Client.objects.all()
    clients_data = []

    for client in clients:
        prospect = Prospect.objects.get(idprospect=client.idprospect_id)
        total_dossiers = Dossier.objects.filter(idprospect=prospect).count()
        
        clients_data.append({
            'client': client,
            'prospect': prospect,
            'total_dossiers': total_dossiers,
        })

    return render(request, 'pages-clients.html', {'clients_data': clients_data})



#----------------------------------------------------------------------suppression
def supprimer_client(request, client_id):
    client = get_object_or_404(Client, idclient=client_id)
    dossiers = Dossier.objects.filter(idprospect=client.idprospect)
    dossiers.update(statut='signe_annule')
    client.delete()
    messages.success(request, 'Client et dossiers associés mis à jour avec succès.')
    return redirect('page_clients')


#==================================pages-incident====================================================


from django.shortcuts import render, redirect
from .models import Incident, Client
from django.contrib import messages
from django.utils import timezone

def suivie(request):
    # Récupération des incidents et des clients pour affichage
    incidents = Incident.objects.all()
    clients = Client.objects.all()

    if request.method == 'POST':
        # Récupère les données du formulaire
        dateincident = request.POST.get('dateincident')
        heureincident = request.POST.get('heureincident')
        client_id = request.POST.get('client')
        site = request.POST.get('site')
        description = request.POST.get('description')
        responsabilite = request.POST.get('responsabilite')

        # Crée un nouvel incident avec les données fournies
        client = Client.objects.get(idclient=client_id)
        new_incident = Incident(
            idclient=client,
            site=site,
            description=description,
            responsabilite=responsabilite,
            dateincident=dateincident,
            heureincident=heureincident,
            dateenregistrement=timezone.now()
        )
        new_incident.save()
        messages.success(request, 'Incident enregistré avec succès !')
        return redirect('suivie')

    return render(request, 'pages-suivie.html', {'incidents': incidents, 'clients': clients})




#-----------------------------------modification -------


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Incident
import json
@csrf_exempt
def modifier_incident(request, incident_id):
    if request.method == 'PUT':
        try:
            # Récupérer l'incident à modifier
            incident = Incident.objects.get(idincident=incident_id)
            
            # Extraire les données du corps de la requête
            data = json.loads(request.body.decode('utf-8'))
            
            # Utiliser les attributs corrects du modèle
            incident.dateincident = data.get('Date_incident', incident.dateincident)
            incident.heureincident = data.get('heureincident', incident.heureincident)
            incident.idclient_id = data.get('client', incident.idclient_id)  # Mettre à jour la clé étrangère
            incident.site = data.get('Site', incident.site)
            incident.description = data.get('description', incident.description)
            incident.responsabilite = data.get('responsabilite', incident.responsabilite)

            # Sauvegarder les modifications
            incident.save()
            
            return JsonResponse({'status': 'success', 'message': 'Incident modifié avec succès.'}, status=200)
        except Incident.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Incident introuvable.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Données JSON invalides.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


#-----------------------------------   suppression   ---------------------
from django.http import JsonResponse
from .models import Incident

def supprimer_incident(request, incident_id):
    if request.method == 'DELETE':
        try:
            incident = Incident.objects.get(idincident=incident_id)
            incident.delete()  # Supprimer l'incident
            return JsonResponse({'status': 'success', 'message': 'Incident supprimé avec succès.'}, status=200)
        except Incident.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Incident introuvable.'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)



#===================================================gestion data =======================================

from django.shortcuts import render

def datas(request):
    # Récupérer toutes les données de recharge et les prospects
    datas = Data.objects.all()
    prospects = Prospect.objects.all()
    return render(request, 'pages-data.html', {'datas': datas, 'prospects': prospects, 'user': request.user})

from django.contrib import messages
from django.shortcuts import redirect, render
from datetime import datetime, timedelta
from .models import Data, Prospect
from django.utils import timezone

def data_create(request):
    if request.method == 'POST':
        numerosim = request.POST.get('numerosim')
        volume = request.POST.get('volume')
        site = request.POST.get('site')
        idprospect_id = request.POST.get('idprospect')
        daterecharge = request.POST.get('daterecharge')

        # Calcul de la date d'expiration
        if daterecharge:
            daterecharge_obj = datetime.strptime(daterecharge, "%Y-%m-%d").date()
            dateexpiration = daterecharge_obj + timedelta(days=28)

            # Détermine le statut
            today = timezone.now().date()
            if daterecharge_obj <= today <= dateexpiration:
                statut = 'en_cours'
            else:
                statut = 'depasse'

            # Mise à jour des recharges précédentes
            Data.objects.filter(numerosim=numerosim, statut='en_cours').update(statut='depasse')

            # Enregistrement de l'instance Data avec le statut calculé
            Data.objects.create(
                numerosim=numerosim,
                volume=volume,
                site=site,
                idprospect_id=idprospect_id,
                daterecharge=daterecharge_obj,
                dateexpiration=dateexpiration,
                statut=statut
            )

            # Message de confirmation
            messages.success(request, "La recharge a été ajoutée avec succès.")
            return redirect('datas')

    # Récupère tous les prospects pour les passer au template
    prospects = Prospect.objects.all()
    return render(request, 'pages-data.html', {'prospects': prospects})


#-----------------------------------suppression----------------------------
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Data

@csrf_exempt
def delete_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Charge les données JSON
            volume = data.get('volume')
            data_instance = Data.objects.get(volume=volume)
            data_instance.delete()
            return JsonResponse({'success': True})
        except Data.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Recharge non trouvée.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Erreur de format des données.'})
    return JsonResponse({'success': False, 'error': 'Requête non autorisée.'})


#-----------------------------------modification----------------------------

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Data
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
def edit_data(request):
    if request.method == 'POST':
        try:
            # Récupération de `numrecharge` à partir de la requête
            numrecharge = request.POST.get('numrecharge')
            logger.debug(f"Numrecharge reçu : {numrecharge}")
            
            # Vérification de la présence de `numrecharge`
            if not numrecharge:
                logger.error("Numrecharge non fourni.")
                return JsonResponse({'success': False, 'error': 'Numrecharge non fourni.'})
            
            # Récupération de l'objet `Data` en fonction de `numrecharge`
            data = Data.objects.get(numrecharge=numrecharge)
            logger.debug(f"Données trouvées : {data}")

            # Mise à jour des champs avec les données du formulaire
            data.site = request.POST.get('site', data.site)
            data.numerosim = request.POST.get('simNumber', data.numerosim)
            data.volume = request.POST.get('volume', data.volume)
            data.idprospect_id = request.POST.get('idprospect', data.idprospect_id)
            
            # Conversion des dates en objets `date`
            daterecharge_str = request.POST.get('rechargeDate')
            dateexpiration_str = request.POST.get('expirationDate')
            if daterecharge_str:
                data.daterecharge = datetime.strptime(daterecharge_str, '%Y-%m-%d').date()
            if dateexpiration_str:
                data.dateexpiration = datetime.strptime(dateexpiration_str, '%Y-%m-%d').date()
            
            # Sauvegarde de l'objet mis à jour
            data.save()

            return JsonResponse({'success': True})
        
        except Data.DoesNotExist:
            logger.error("Recharge non trouvée.")
            return JsonResponse({'success': False, 'error': 'Recharge non trouvée.'})
        
        except Exception as e:
            logger.exception("Erreur lors de la modification.")
            return JsonResponse({'success': False, 'error': f'Erreur interne : {str(e)}'})
    
    logger.warning("Requête non autorisée.")
    return JsonResponse({'success': False, 'error': 'Requête non autorisée.'})
