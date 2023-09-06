from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .forms import *
from .models import *
import json
import requests

# Create your views here.

#enum des tatus
STATUS = {
    0: "En demande",
    1: "En cours",
    2: "Terminée",
    3: "Annulée"
}
    

def index(request):
    offres = Offre.objects.exclude(echange__status=1)
    return render(request, 'rers/index.html', {'offres': offres})

def profil(request):
    utilisateur = request.user
    if not utilisateur.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour accéder à votre profil.")
        return redirect('login')
    
    try:
        savoirs_offerts = Offre.objects.filter(id_user=utilisateur.id)
        demandes_recues = Echange.objects.filter(id_offre__id_user=utilisateur.id)
        demandes_envoyees = Echange.objects.filter(demande_by=utilisateur.id)
    except Offre.DoesNotExist:
        savoirs_offerts = None
    except Echange.DoesNotExist:
        demandes_recues = None
        demandes_envoyees = None    


    return render(request, 'rers/profil.html', {'savoirs_offerts': savoirs_offerts, 'demandes_recues': demandes_recues, 'demandes_envoyees': demandes_envoyees, 'STATUS': STATUS})

def ajout_savoir(request):
    return render(request, 'rers/ajout_savoir.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS , "L'utilisateur a été ajouté avec succès, vous pouvez vous connecter.")
            return redirect('login')
   
    form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})






### API ###


def delete_offer(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        offre = Offre.objects.get(id=id, id_user=request.user.id)
    except Offre.DoesNotExist:
        return Http404("Offre does not exist")

    offre.delete()
    messages.add_message(request, messages.SUCCESS , f"L'offre a été supprimée avec succès.")
    return redirect('profil')

def modify_status_offer(request, id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour modifier le statut d'un échange.")
        return redirect('login')
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            echange = Echange.objects.get(id=id)
        except Echange.DoesNotExist:
            return Http404("Echange does not exist")
        echange.status = status
        echange.save()
        messages.add_message(request, messages.SUCCESS , f"Le statut de l'échange a été modifié avec succès.")
    return redirect('profil')
    

def delete_ask(request, id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour modifier le statut d'un échange.")
        return redirect('login')
    try:
        echange = Echange.objects.get(id=id)
    except Echange.DoesNotExist:
        return Http404("Echange does not exist")
    if (echange.demande_by.id != request.user.id):
        return redirect('profil')
        ###TODO MESSAGE FLASH ERREUR
    echange.delete()
    return redirect('profil')


def add_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Code to be executed if the user is an admin and is authenticated

    
        response = requests.get('https://randomapi.com/api/dd38fe552c2d0f1bbc112a619e6a8b86')
        data = response.json()
        utilisateur = data['results'][0]["customer"]
        user = User.objects.create_user(username=utilisateur["username"], password=utilisateur["password"], email=utilisateur["email"], first_name=utilisateur["name"].split(" ")[0], last_name=utilisateur["name"].split(" ")[1])
        
        
        user.save()
        messages.add_message(request, messages.SUCCESS , f"L'utilisateur {user.username} a été ajouté avec succès")
        return redirect('profil')
    else:
        messages.add_message(request, messages.INFO , "Vous devez être connecté en tant qu'administrateur pour ajouter un utilisateur.")
        return redirect('index')
        
    
    