from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Importe le fichier views depuis le dossier courant
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profil/', views.profil, name='profil'),
    path('accounts/signup/', views.register, name='register'),
    path('add-offer/', views.add_offer, name='add_offer'),
    path('add-know/', views.add_know, name='add_know'),
    path('details-offer/<int:id>', views.details_offer, name='details_offer'),
    path('api/add-ask/<int:id>', views.add_ask, name='add_ask'),
    path('api/delete-offer/<int:id>', views.delete_offer, name='delete_offer'),
    path('api/modify-status-offer/<int:id>', views.modify_status_offer, name='modify_status_offer'),
    path('api/delete-ask/<int:id>', views.delete_ask, name='delete_ask'),
    path('api/add-user', views.add_user, name='add_user'),
]
