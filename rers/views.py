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

def add_offer(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour ajouter une offre.")
        return redirect('login')
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            # Vérifier si l'utilisateur offre déjà le savoir
            if Offre.objects.filter(id_user=request.user, id_savoir=form.cleaned_data['id_savoir']).exists():
                messages.add_message(request, messages.WARNING , "Vous offrez déjà ce savoir.")
                return redirect('add_offer')
            offre = form.save(commit=False)
            offre.id_user = request.user
            offre.save()
            messages.add_message(request, messages.SUCCESS , "L'offre a été ajoutée avec succès.")
            return redirect('profil')
    else:
        form = OffreForm()
    return render(request, 'rers/add-offer.html', {'form': form})

def add_know(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour ajouter un savoir.")
        return redirect('login')
    if request.method == 'POST':
        form = SavoirForm(request.POST)
        if form.is_valid():
            savoir = form.save(commit=False)
            savoir.id_user = request.user
            savoir.save()
            messages.add_message(request, messages.SUCCESS , "Le savoir a été ajouté avec succès.")
            return redirect('profil')
    else:
        form = SavoirForm()
    return render(request, 'rers/add-know.html', {'form': form})

def details_offer(request, id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour voir les détails d'une offre.")
        return redirect('login')
    try:
        offre = Offre.objects.get(id=id)
        echanges = Echange.objects.filter(id_offre=offre)
        utilisateurs = [echange.demande_by for echange in echanges]
        offres_utilisateur = Offre.objects.filter(id_user=request.user)
    except Offre.DoesNotExist:
        raise Http404("L'offre n'existe pas.")
    except Echange.DoesNotExist:
        echanges = None
        utilisateurs = None
        offres_utilisateur = None

    user_in_list = request.user in utilisateurs
    return render(request, 'rers/details-offer.html', {'offre': offre, 'echanges': echanges, 'user_in_list': user_in_list, 'offres_utilisateur': offres_utilisateur, 'STATUS': STATUS})




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS , "L'utilisateur a été ajouté avec succès, vous pouvez vous connecter.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})






### API ###


def delete_offer(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        offre = Offre.objects.get(id=id, id_user=request.user.id)
    except Offre.DoesNotExist:
        raise Http404("L'offre n'existe pas.")

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
            raise Http404("L'Echange n'existe pas.")
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
        raise Http404("L'échange n'existe pas.")
    if (echange.demande_by.id != request.user.id):
        messages.add_message(request, messages.INFO , "Vous ne pouvez pas supprimer une demande qui ne vous appartient pas.")
        return redirect('profil')
    echange.delete()
    messages.add_message(request, messages.SUCCESS , f"La demande a été supprimée avec succès.")
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
        
    
def add_ask(request, id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO , "Vous devez être connecté pour ajouter une demande.")
        return redirect('login')
    try:
        offre = Offre.objects.get(id=id)
    except Offre.DoesNotExist:
        raise Http404("L'offre n'existe pas.")
    if (offre.id_user.id == request.user.id):
        messages.add_message(request, messages.INFO , "Vous ne pouvez pas faire une demande sur votre propre offre.")
        return redirect('profil')
    
    try:
        echanges_utilisateur = Echange.objects.filter(demande_by=request.user)
    except Echange.DoesNotExist:
        echanges_utilisateur = None

    if echanges_utilisateur.filter(id_offre=offre).exists():
        messages.add_message(request, messages.INFO , "Vous avez déjà fait une demande pour cette offre.")
        return redirect('profil')
    
    echange = Echange(id_offre=offre, demande_by=request.user)
    echange.save()
    messages.add_message(request, messages.SUCCESS , "La demande a été ajoutée avec succès.")
    return redirect('profil')