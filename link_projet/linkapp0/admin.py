from django.contrib import admin

from django.contrib import admin
from .models import Agent, Client, Prospect, Incident, Dossier, Data

# Enregistrement des modèles dans l'admin
admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Prospect)
admin.site.register(Incident)
admin.site.register(Dossier)
admin.site.register(Data)




#class DataAdmin(admin.ModelAdmin):
    # Spécifie les champs à afficher dans la liste des objets
    #list_display = ('numrecharge', 'numerosim', 'site', 'idprospect', 'volume', 'daterecharge', 'dateexpiration', 'statut')

    # Rend les champs calculés en lecture seule dans l'interface d'administration
    #readonly_fields = ('dateexpiration', 'statut')

    # Surcharge de la méthode save_model pour s'assurer que les champs sont mis à jour correctement
   # def save_model(self, request, obj, form, change):
        # Appelle la méthode save du modèle pour gérer la logique automatique
        #obj.save()

#admin.site.register(Data, DataAdmin)
