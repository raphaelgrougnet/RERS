from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Savoir(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    nom = models.CharField(max_length=150)
    description = models.TextField()
    def __str__(self):
        return self.nom
    
class Offre(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_savoir = models.ForeignKey(Savoir, on_delete=models.CASCADE)
    def __str__(self):
        return self.id_user.username + " " + self.id_savoir.nom

class Echange(models.Model):
    demande_by = models.ForeignKey(User, on_delete=models.CASCADE)
    id_offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    CHOICES = ((0, 'En demande'), (1, 'En cours'), (2, 'Terminé'), (3, 'Annulé'))
    status = models.IntegerField(choices=CHOICES, default=0)
    def __str__(self):
        return self.demande_by.username + " " + self.id_offre.id_savoir.nom + " " + self.id_offre.id_user.username
    





