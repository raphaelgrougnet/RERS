from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Offre, Savoir

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name",  "last_name", "email", "password1", "password2")

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
    def clean_nom(self):
        data = self.cleaned_data['nom']
        print(data)
        if Savoir.objects.filter(nom=data).exists():
            raise forms.ValidationError("Ce savoir existe déjà.")
        return data    
