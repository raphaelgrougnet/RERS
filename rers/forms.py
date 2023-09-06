from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Offre, Savoir

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['id_savoir']
        labels = {
            'id_savoir': 'Savoir que vous voulez offrir'
        }
        
class SavoirForm(forms.ModelForm):
    class Meta:
        model = Savoir
        fields = ['nom', 'description']
        labels = {
            'nom': 'Nom du savoir',
            'description': 'Description du savoir'
        }